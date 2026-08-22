#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct _Z3_config *Z3_config;
typedef struct _Z3_context *Z3_context;
extern Z3_config Z3_mk_config(void);
extern void Z3_del_config(Z3_config c);
extern Z3_context Z3_mk_context(Z3_config c);
extern void Z3_del_context(Z3_context c);
extern const char *Z3_get_full_version(void);
extern const char *Z3_eval_smtlib2_string(Z3_context c, const char *str);

int main(int argc, char **argv) {
    if (argc == 2 && strcmp(argv[1], "--version") == 0) {
        printf("%s\n", Z3_get_full_version());
        return 0;
    }
    FILE *f = stdin;
    if (argc > 2) { fprintf(stderr, "usage: %s [file.smt2]\n", argv[0]); return 2; }
    if (argc == 2) { f = fopen(argv[1], "rb"); if (!f) { perror("fopen"); return 2; } }
    size_t cap = 8192, len = 0;
    char *buf = (char*)malloc(cap);
    if (!buf) return 2;
    for (;;) {
        if (len + 4096 + 1 > cap) { cap *= 2; char *tmp = realloc(buf, cap); if (!tmp) return 2; buf = tmp; }
        size_t n = fread(buf + len, 1, 4096, f); len += n;
        if (n < 4096) { if (ferror(f)) { perror("fread"); return 2; } break; }
    }
    if (argc == 2) fclose(f);
    buf[len] = '\0';
    Z3_config cfg = Z3_mk_config();
    Z3_context ctx = Z3_mk_context(cfg);
    Z3_del_config(cfg);
    fprintf(stderr, "%s\n", Z3_get_full_version());
    const char *out = Z3_eval_smtlib2_string(ctx, buf);
    if (out) fputs(out, stdout);
    Z3_del_context(ctx);
    free(buf);
    return 0;
}
