/* archive.i */
%module _myemsl_archive
%{
#include <archive.h>
#include <archive_entry.h>

//For some reason, this isn't defined in the library.
int archive_entry_acl_next_w(struct archive_entry *e, int want_type, int *type, int *permset, int *tag, int *qual, const wchar_t **name)
{
        return 0;
}

int myemsl_archive_entry_filetype(struct archive_entry *ae)
{
        return archive_entry_filetype(ae);
}

int myemsl_archive_read_data(struct archive *a, char *d, int *s)
{
        int res = archive_read_data(a, d, *s);
        if(res < 0)
        {
                *s = 0;
        }
        else
        {
                *s = res;
                res = 0;
        }
        return res;
}

%}

%include <cstring.i>
typedef long time_t;
%include <archive.h>
%include <archive_entry.h>

%cstring_output_withsize(char *d, int *s);
int myemsl_archive_read_data(struct archive *a, char *d, int *s);
int myemsl_archive_entry_filetype(struct archive_entry *ae);

