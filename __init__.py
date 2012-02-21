
from cloudservers import CloudServers, ServerManager, ImageManager, CloudServersException, Server
from time import sleep
class chef_vpc:

    def __init__(self):
        filename = '/tmp/.rackspace_cloud_account'
        self._setup_cloud_instances(filename)
        server = self._create_server()
        print server.id
        self._get_server_status(server.id)
        print "Finished"
        
    def _throw_exception(self, exception):
        print "Cloud Servers had an exception."
        print exception
        
    def _setup_cloud_instances(self, filename):
        _creds = self._read_to_dict(filename)
        self.cloudservers = CloudServers(_creds['userid'], _creds['api_key'])
        self.imageManager = ImageManager(self.cloudservers)
        self.serverManager = ServerManager(self.cloudservers)

    def _get_list_of_current_servers(self):
        cur_servers = {}
        try:
            cur_servers = self.cloudservers.servers.list()
        except CloudServersException as exception:
            self._throw_exception(exception)
        return cur_servers
        
    def _get_list_of_server_images(self):
        server_images = {}
        try:
            server_images = ImageManager(self.cloudservers).list()
        except CloudServersException as exception:
            self._throw_exception(exception)
        return server_images
        
    def _read_to_dict(self, filename):
        fileHandle = file(filename, 'r')
        line = fileHandle.readline()
        dictName = {}
        keycounter = 1
        while line:
            l = line.split(': ')
            if len(l) > 1:
                key = l[0]
                l[1] = l[1].replace("\n","")
                dictName[key] = l[1]
            line = fileHandle.readline()
        return dictName

    def _create_server(self):
        print "creating server"
        server = ""
        try:
            server = self.serverManager.create("firsttest4", 51, 2)
        except CloudServersException as exception:
            self._throw_exception(exception)
        return server
        
    def _get_server_status(self, server_id):
        server = self.serverManager.get(server_id)
        status = ""
        while status != "ACTIVE":
            try:
                print "Progress of server %s is %d"%(server.name, progress)
                print "Status is: '%s'"%server.status
                sleep(15)
                server = self.serverManager.get(server_id)
                status = server.status
                progress = server.progress
            except:
                sleep(15)
                server = self.serverManager.get(server_id)
                status = server.status
                progress = server.progress
        print "Progress of server %s is %d"%(server.name, progress)
        print "Status is: %s"%server.status

if __name__ == '__main__':
    chef = chef_vpc()
