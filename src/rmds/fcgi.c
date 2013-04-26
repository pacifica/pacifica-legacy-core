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

void internal_error(FCGX_Request *req)
{
	return_header(req, 500, "Something bad happened", "application/json");
	FCGX_Finish_r(req);
}
void bad_request_error(FCGX_Request *req)
{
	return_header(req, 400, "Bad input", "application/json");
	FCGX_Finish_r(req);
}

void *process(void *a)
{
	char **envp;
	char *data;
	char *str;
	long to_process;
	long offset;
	int res;
	FCGX_Request req;
	json_object *json;
	FCGX_InitRequest(&req, 0, 0);
	while(1)
	{
		res = FCGX_Accept_r(&req);
		if(res < 0)
		{
			break;
		}
		str = FCGX_GetParam("REQUEST_METHOD", req.envp);
		if(!str)
		{
			bad_request_error(&req);
			continue;
		}
		if(!strcmp(str, "POST") || !strcmp(str, "PUT"))
		{
			str = FCGX_GetParam("CONTENT_LENGTH", req.envp);
			if(!str)
			{
				bad_request_error(&req);
				continue;
			}
			to_process = strtol(str, NULL, 10);
			if(to_process > MAX_UPLOAD)
			{
				bad_request_error(&req);
				continue;
			}
			data = malloc(sizeof(char) * to_process);
			if(!data)
			{
				internal_error(&req);
				continue;
			}
			res = FCGX_GetStr(data, to_process, req.in);
			if(res != to_process)
			{
				bad_request_error(&req);
				free(data);
				continue;
			}
			json = json_tokener_parse(data);
			if(!json)
			{
				bad_request_error(&req);
				free(data);
				continue;
			}
			json_object_put(json);
			free(data);
		}

		str = FCGX_GetParam("REQUEST_URI", req.envp);
		if(!str)
		{
			bad_request_error(&req);
			continue;
		}
		return_header(&req, 200, NULL, "application/json");
		FCGX_FPrintF(req.out, "{\n");
//FIXME jsonurlencode...
		FCGX_FPrintF(req.out, "\"URL\": \"%s\",\n", str);
		FCGX_FPrintF(req.out, "\"ENV\": [\n");

		for(envp = req.envp; *envp != NULL; envp++)
		{
//FIXME jsonurlencode...
			FCGX_FPrintF(req.out, "\"%s\"", *envp);
			if(envp[1] != NULL)
			{
				FCGX_FPrintF(req.out, ",\n", *envp);
			}
			else
			{
				FCGX_FPrintF(req.out, "]}\n", *envp);
			}
		}
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
