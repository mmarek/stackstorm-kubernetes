import json

from lib.k8s import K8sClient


class readStorageV1beta1StorageClass(K8sClient):

    def run(
            self,
            name,
            config_override=None,
            exact=None,
            export=None,
            pretty=None):

        rc = False

        args = {}
        args['config_override'] = {}
        args['pretty'] = ''

        if name is not None:
            args['name'] = name
        else:
            return (False, "name is a required parameter")
        if config_override is not None:
            args['config_override'] = config_override
        if exact is not None:
            args['exact'] = exact
        if export is not None:
            args['export'] = export
        if pretty is not None:
            args['pretty'] = pretty
        if 'body' in args:
            args['data'] = args['body']
        args['headers'] = {'Content-type': u'application/json', 'Accept': u'application/json, application/yaml, application/vnd.kubernetes.protobuf'}  # pylint: disable=line-too-long
        args['url'] = "apis/storage.k8s.io/v1beta1/storageclasses/{name}".format(name=name )
        args['method'] = "get"

        self.addArgs(**args)
        self.makeRequest()

        myresp = {}
        myresp['status_code'] = self.resp.status_code
        myresp['data'] = json.loads(self.resp.content.rstrip())

        if myresp['status_code'] >= 200 and myresp['status_code'] <= 299:
            rc = True

        return (rc, myresp)