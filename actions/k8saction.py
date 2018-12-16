import json
import kubernetes.client
from lib.k8s import K8sClient
from lib.util import json_serial
from kubernetes.client.rest import ApiException


class K8sActionRunner(K8sClient):

    def run(
            self,
            service,
            action_name,
            params=None,
            config_override=None):

        configuration = self.get_k8s_config(config_override)

        # create an instance of the API class
        api_instance = getattr(kubernetes.client, service)(
            kubernetes.client.ApiClient(configuration))()

        try:
            # check if the body contains and object or a string
            # if a string instantiate the instance from the string
            if hasattr(params, 'body') and params.body == str:
                params.body = getattr(kubernetes.client, params.body)()

            api_response = getattr(api_instance, action_name)(**params)
            response = json.loads(json.dumps(
                api_response, default=json_serial))

            return(True, response)
        except ApiException as e:

            erro_str = ("Exception when calling %s->%s: %s\n" %
                        service, action_name, e)
            print(erro_str)

            return (False, json.loads(json.dumps(
                erro_str, default=json_serial)))