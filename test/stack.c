#include <stdlib.h>
#ifndef ___home_lavrut_f_rendu_kooc_test_stack
# define ___home_lavrut_f_rendu_kooc_test_stack
# include "/home/lavrut_f/rendu/kooc/test/stack.h"
#endif
void ___6system___5stack__8callable__11constructor(___6system__4type__5stack this, __6vtable___6system__4type__5stack vtable, char *type, void *ptr)
{
    vtable->___6system___5stack__8callable__9push_back = &___6system___5stack__7virtual__9push_back;
    vtable->___6system___5stack__8callable__8pop_back = &___6system___5stack__7virtual__8pop_back;
    this->___6system___5stack__8variable__5_type = type;
    ;
    this->___6system___5stack__8variable__4_ptr = ptr;
    ;
    this->___6system___5stack__8variable__5_next = NULL;
    ;
}
int ___6system___5stack__7virtual__9push_back(___6system__4type__5stack this, char *type, void *ptr)
{
    stack * tmp = this;
    while (tmp)
        tmp = tmp->_next;
        ;
    tmp->_next = new(type, ptr);
    ;
    return 0;
}
int ___6system___5stack__8callable__9push_back(___6system__4type__5stack this, char *type, void *ptr)
{
    __6vtable___6system__4type__5stack *vtable = ((void *) this) - 8;
    return (int) ((*vtable)->___6system___5stack__8callable__9push_back)(this, type, ptr);
}
int ___6system___5stack__7virtual__8pop_back(___6system__4type__5stack this)
{
    stack * tmp = this;
    while (tmp && this->_next;
     && this->_next;
    ->_next;
    )
        tmp = tmp->_next;
        ;
    if (!tmp->_next;
    )
        return 1;
    tmp->_next = NULL;
    return 0;
}
int ___6system___5stack__8callable__8pop_back(___6system__4type__5stack this)
{
    __6vtable___6system__4type__5stack *vtable = ((void *) this) - 8;
    return (int) ((*vtable)->___6system___5stack__8callable__8pop_back)(this);
}
___6system__4type__5stack ___6system___5stack__8callable__3new(char *type, void *ptr)
{
    ___6system__4type__5stack this;
    __6vtable___6system__4type__5stack *vtable;
    this = sizeof (void *) + malloc(sizeof (void *) + sizeof (*this));
    vtable = ((void *) this) - sizeof (void *);
    *vtable = malloc(sizeof (**vtable));
    ___6system___5stack__8callable__11constructor(this, *vtable, type, ptr);
    return this;
}
int main()
{
    char *ptr = "test";
    ___6system__4type__5stack *test = ___6system___5stack__8callable__3new("char*", ptr);
}

