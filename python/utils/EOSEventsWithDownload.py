from DataFormats.FWLite import Events as FWLiteEvents
from CMGTools.Production.changeComponentAccessMode import convertFile as convertFileAccess 
import os, subprocess, json, timeit, hashlib
from socket import gethostname
from re import sub

class EOSEventsWithDownload(object):
    def __init__(self, files, tree_name):
        self.aggressive = getattr(self.__class__, 'aggressive', 0)
        self.long_cache = getattr(self.__class__, 'long_cache', False)
        print "[FileFetcher]: Aggressive prefetching level %d" % self.aggressive
        self._files = []
        self._nevents = 0
        try:
            query = ["edmFileUtil", "--ls", "-j"]+[("file:"+f if f[0]=="/" else f) for f in files]
            retjson = subprocess.check_output(query)
            retobj = json.loads(retjson)
            for entry in retobj:
                self._files.append( (str(entry['file']), self._nevents, self._nevents+entry['events'] ) ) # str() is needed since the output is a unicode string
                # self._files.append( (sub('root://cms-xrd-global.cern.ch/', 'root://xrootd-cms.infn.it/', str(entry['file'])), self._nevents, self._nevents+entry['events'] ) )
                self._nevents += entry['events']
            # from pdb import set_trace; print self._files; set_trace()
        except subprocess.CalledProcessError:
            print "[FileFetcher]: Failed the big query: ",query
            ## OK, now we go for something more fancy
            for f in files:
                print "[FileFetcher]: Try file: ",f
                OK = False
                # step 1: try the local query
                if f[0] == "/":
                    urls = [ 'file:'+f ] 
                else:
                    urls = [ f ] # one retry
                    try:
                        # then try the two main redirectors, and EOS again
                        if "/store/data" in f and "PromptReco" in f:
                            urls.append( convertFileAccess(f,  "root://eoscms.cern.ch//eos/cms/tier0%s") )
                        urls.append( convertFileAccess(f,  "root://xrootd-cms.infn.it/%s") )
                        urls.append( convertFileAccess(f,  "root://cmsxrootd.fnal.gov/%s") )
                        urls.append( convertFileAccess(f,  "root://cms-xrd-global.cern.ch/%s") )
                        urls.append( convertFileAccess(f,  "root://eoscms.cern.ch//eos/cms%s") )
                    except:
                        pass
                for u in urls:
                    print "[FileFetcher]: Try url: ",u
                    try:
                        query = ["edmFileUtil", "--ls", "-j", u]
                        retjson = subprocess.check_output(query)
                        retobj = json.loads(retjson)
                        for entry in retobj:
                            self._files.append( (str(entry['file']), self._nevents, self._nevents+entry['events'] ) ) # str() is needed since the output is a unicode string
                            self._nevents += entry['events']
                        OK = True
                        print "[FileFetcher]: Successful URL ",u
                        break
                    except:
                        print "[FileFetcher]: Failed the individual query: ",query
                        pass
                if not OK:
                    if self.aggressive == 3 and "/store/mc" in f:
                        print "[FileFetcher]: Will skip file ",f
                        continue
                    raise RuntimeError, "Failed to file %s in any way. aborting job " % f
                else:
                    print self._files
        if self.aggressive == 3 and self._nevents == 0:
            raise RuntimeError, "Failed to find all files for this component. aborting job "
        self._fileindex = -1
        self._localCopy = None
        self.events = None
        ## Discover where I am
        self.inMeyrin = True
        if 'LSB_JOBID' in os.environ and 'HOSTNAME' in os.environ and self.aggressive == 1:
            hostname = os.environ['HOSTNAME'].replace(".cern.ch","")
            try:
                wigners = subprocess.check_output(["bmgroup","g_wigner"]).split()
                if hostname in wigners:
                    self.inMeyrin = False
                    print "[FileFetcher]: Host %s is in bmgroup g_wigner, so I assume I'm in Wigner and not Meyrin" % hostname
            except:
                pass
        ## How aggressive should I be?
        # 0 = default; 1 = always fetch from Wigner; 2 = always fetch from anywhere if it's a xrootd url
    def __len__(self):
        return self._nevents
    def __getattr__(self, key):
        return getattr(self.events, key)
    def isLocal(self,filename):
        if self.aggressive == -2: return True
        if filename.startswith("root://") and not filename.startswith("root://eoscms"):
            return False # always prefetch AAA
        if self.aggressive == -1: return True
        if self.aggressive >= 2: return False
        if self.aggressive >= 1 and not self.inMeyrin: return False
        fpath = filename.replace("root://eoscms.cern.ch//","/").replace("root://eoscms//","/")
        if "?" in fpath: fpath = fpath.split["?"][0]
        try:
            finfo = subprocess.check_output(["eos", "fileinfo", fpath])
            replicas = False
            nears    = False
            for line in finfo.split("\n"):
                if line.endswith("geotag"):
                    replicas = True
                elif replicas and ".cern.ch" in line:
                    geotag = int(line.split()[-1])
                    print "[FileFetcher]: Found a replica with geotag %d" % geotag
                    if self.inMeyrin:
                        if geotag > 9000: return False # far replica: bad (EOS sometimes gives the far even if there's a near!)
                        else: nears = True # we have found a replica that is far away
                    else:
                        if geotag < 1000: return False # far replica: bad (EOS sometimes gives the far even if there's a near!)
                        else: nears = True # we have found a replica that is far away
            # if we have found some near replicas, and no far replicas
            if nears: return True
        except:
            pass
        # we don't know, so we don't transfer (better slow than messed up)
        return True
    def __getitem__(self, iEv):
        if self._fileindex == -1 or not(self._files[self._fileindex][1] <= iEv and iEv < self._files[self._fileindex][2]):
            self.events = None # so it's closed
            if self._localCopy:
                print "[FileFetcher]: Removing local cache file %s" % self._localCopy
                try:
                    os.remove(self._localCopy)
                except:
                    pass
                self._localCopy = None
            for i,(fname,first,last) in enumerate(self._files):
                if first <= iEv and iEv < last:
                    print "[FileFetcher]: For event range [ %d, %d ) will use file %r " % (first,last,fname)
                    self._fileindex = i
                    if fname.startswith("root://eoscms") or (self.aggressive >= 2 and fname.startswith("root://")):
                        if not self.isLocal(fname):
                            tmpdir = os.environ['TMPDIR'] if 'TMPDIR' in os.environ else "/tmp"
                            # VS 29/10/19, /scratch is larger than /tmp for T3 WN:
                            from pdb import set_trace
                            # from getpass import getuser; USER = getuser()
                            # if 't3' in gethostname(): tmpdir = "/scratch" 
                            # if 't3' in gethostname(): tmpdir = "/work/%s/tmp" %USER
                            # if 't3' in gethostname(): tmpdir = 'root://t3dcachedb03.psi.ch/pnfs/psi.ch/cms/trivcat/store/user/vstampf/hnl_tmp/'
                            if 't3' in gethostname(): tmpdir = 'root://t3se01.psi.ch/pnfs/psi.ch/cms/trivcat/store/user/vstampf/hnl_tmp/'
                            rndchars  = "".join([hex(ord(i))[2:] for i in os.urandom(8)]) if not self.long_cache else "long_cache-id%d-%s" % (os.getuid(), hashlib.sha1(fname).hexdigest());
                            localfile = "%s/%s-%s.root" % (tmpdir, os.path.basename(fname).replace(".root",""), rndchars)
                            file_name_simple = os.path.basename(fname)
                            if self.long_cache and os.path.exists(localfile):
                                print "[FileFetcher]: Filename %s is already available in local path %s " % (fname,localfile)
                                fname = localfile
                            else:
                                try:
                                    print "[FileFetcher]: Filename %s is remote (geotag >= 9000), will do a copy to local path %s " % (fname,localfile)
                                    start = timeit.default_timer()
                                    # set_trace()
                                    print subprocess.check_output(["xrdcp","-f","-N",fname,localfile])
                                    print "[FileFetcher]: Time used for transferring the file locally: %s s" % (timeit.default_timer() - start)
                                    if not self.long_cache: self._localCopy = localfile 
                                    fname = localfile
                                except:
                                    print "[FileFetcher]: Could not save file locally, will run from remote"
                                    if 't3' in gethostname(): 
                                        os.system("uberftp t3se01.psi.ch 'rm /pnfs/psi.ch/cms/trivcat/store/user/vstampf/hnl_tmp/%s'" %file_name_simple)
                                    else:
                                        if os.path.exists(localfile): os.remove(localfile) # delete in case of incomplete transfer
                    print "[FileFetcher]: Will run from "+fname
                    self.events = FWLiteEvents([fname])
                    break
        self.events.to(iEv - self._files[self._fileindex][1])
        return self
    def endLoop(self):
        if '_localCopy' not in self.__dict__:
            return
        todelete = self.__dict__['_localCopy']
        if todelete:
            print "[FileFetcher]: Removing local cache file ",todelete
            if 't3' in gethostname(): os.system("uberftp t3se01.psi.ch 'rm /pnfs/psi.ch/cms/trivcat/store/user/vstampf/hnl_tmp/%s'" % os.path.basename(todelete))
            else: os.remove(todelete)
    def __del__(self):
        self.endLoop()

