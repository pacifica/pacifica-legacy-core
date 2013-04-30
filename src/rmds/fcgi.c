#include <stdlib.h>
#include <malloc.h>
#include <string.h>
#include <fcgiapp.h>
#include <json.h>

#define MAX_UPLOAD (1024 * 1024 * 10)
#define URL_PREFIX "/myemsl/api/1/rmds/"

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
	char *tstr;
	char *tstr2;
	char *method;
	const char *cstr;
	long to_process;
	long offset;
	long item_id;
	int res;
	FCGX_Request req;
	json_object *json;
	json_object *json_out;
	FCGX_InitRequest(&req, 0, 0);
	while(1)
	{
		res = FCGX_Accept_r(&req);
		if(res < 0)
		{
			break;
		}
		method = FCGX_GetParam("REQUEST_METHOD", req.envp);
		if(!method)
		{
			bad_request_error(&req);
			continue;
		}
		json_out = json_object_new_object();
		if(!json_out)
		{
			bad_request_error(&req);
			continue;
		}
		str = FCGX_GetParam("REQUEST_URI", req.envp);
		if(!str)
		{
			bad_request_error(&req);
			json_object_put(json_out);
			continue;
		}
		if(strncmp(str, URL_PREFIX, strlen(URL_PREFIX)))
		{
			bad_request_error(&req);
			json_object_put(json_out);
			continue;
		}
		tstr = strchr(str + strlen(URL_PREFIX), '/');
		if(!tstr)
		{
			bad_request_error(&req);
			json_object_put(json_out);
			continue;
		}
		/* str + strlen(URL_PREFIX) to tstr is now the uuid of the instance. */
		for(tstr2 = tstr + 1; *tstr2 != '\0' && (*tstr2 >= '0' && *tstr2 <= '9'); tstr2++);
		if(tstr2 == tstr + 1 || (*tstr2 != '\0' && *tstr2 != '?'))
		{
			bad_request_error(&req);
			json_object_put(json_out);
			continue;
		}
		/* tstr + 1 to tstr2 is item_id. */
		item_id = strtol(tstr + 1, NULL, 10);
		json_object_object_add(json_out, "REQUEST_URL", json_object_new_string(str));
		json_object_object_add(json_out, "ITEM_ID", json_object_new_int64(item_id));
		if(!strcmp(method, "POST") || !strcmp(method, "PUT"))
		{
			str = FCGX_GetParam("CONTENT_LENGTH", req.envp);
			if(!str)
			{
				bad_request_error(&req);
				json_object_put(json_out);
				continue;
			}
			to_process = strtol(str, NULL, 10);
			if(to_process > MAX_UPLOAD)
			{
				bad_request_error(&req);
				json_object_put(json_out);
				continue;
			}
			data = malloc(sizeof(char) * to_process);
			if(!data)
			{
				internal_error(&req);
				json_object_put(json_out);
				continue;
			}
			res = FCGX_GetStr(data, to_process, req.in);
			if(res != to_process)
			{
				bad_request_error(&req);
				free(data);
				json_object_put(json_out);
				continue;
			}
			json = json_tokener_parse(data);
			if(!json)
			{
				bad_request_error(&req);
				free(data);
				json_object_put(json_out);
				continue;
			}
			json_object_put(json);
			free(data);
		}

		return_header(&req, 200, NULL, "application/json");
		cstr = json_object_to_json_string_ext(json_out, JSON_C_TO_STRING_PRETTY);
		FCGX_FPrintF(req.out, "%s\n", cstr);
		json_object_put(json_out);
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
