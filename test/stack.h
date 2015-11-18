#include <stdlib.h>
typedef struct ___6system__5class__5stack *___6system__4type__5stack;
typedef struct __6vtable___6system__5class__5stack *__6vtable___6system__4type__5stack;
void ___6system___5stack__8callable__11constructor(___6system__4type__5stack, __6vtable___6system__4type__5stack, char *type, void *ptr);
___6system__4type__5stack ___6system___5stack__8callable__3new(char *type, void *ptr);
int ___6system___5stack__7virtual__9push_back(___6system__4type__5stack, char *type, void *ptr);
int ___6system___5stack__8callable__9push_back(___6system__4type__5stack, char *type, void *ptr);
int ___6system___5stack__7virtual__8pop_back(___6system__4type__5stack);
int ___6system___5stack__8callable__8pop_back(___6system__4type__5stack);
struct __attribute__((packed))  __6vtable___6system__5class__5stack {
    int (*___6system___5stack__8callable__9push_back)(___6system__4type__5stack, char *type, void *ptr);
    int (*___6system___5stack__8callable__8pop_back)(___6system__4type__5stack);
    };
struct __attribute__((packed))  ___6system__5class__5stack {
    char *___6system___5stack__8variable__5_type;
    char *___6system___5stack__8variable__4_ptr;
    void *___6system___5stack__8variable__5_next;
    };

