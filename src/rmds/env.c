#include <stdlib.h>
#include <malloc.h>
#include <fcgiapp.h>
#include <json.h>

#define MAX_UPLOAD (1024 * 1024 * 10)

void return_header(FCGX_Request *req, int status, char *status_str, char *content_type)
{
	if(status == 200 && status_str == NULL)
	{
		status_str = "OK";
	}
	FCGX_FPrintF(req->out,
	             "Status: %d %s\r\n"
	             "Content-type: %s\r\n"
	             "\r\n",
	             status,
	             status_str,
	             content_type
	);
}

void *process(void *a)
{
	char **envp;
	const char *data;
	int res;
	FCGX_Request req;
	json_object *json;
	json_object *jarray;
	FCGX_InitRequest(&req, 0, 0);
	while(1)
	{
		res = FCGX_Accept_r(&req);
		if(res < 0)
		{
			break;
		}
		json = json_object_new_object();
		jarray = json_object_new_array();
		return_header(&req, 200, NULL, "application/json");
		for(envp = req.envp; *envp != NULL; envp++)
		{
//FIXME jsonurlencode...
			json_object_array_add(jarray, json_object_new_string(*envp));
		}
		json_object_object_add(json, "env", jarray);
		data = json_object_to_json_string_ext(json, JSON_C_TO_STRING_PRETTY);
		FCGX_FPrintF(req.out, "%s\n", data);
		json_object_put(json);
		FCGX_Finish_r(&req);
	}
	return NULL;
}

int main(int argc, char *argv[])
{
	FCGX_Init();
	process(NULL);
	return 0;
}
