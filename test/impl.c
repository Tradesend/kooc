#include <stdlib.h>
#ifndef ___home_lavrut_f_rendu_kooc_test_klass
# define ___home_lavrut_f_rendu_kooc_test_klass
# include "/home/lavrut_f/rendu/kooc/test/klass.h"
#endif
int ___9NAMESPACE___5CLASS__7virtual__6method(___9NAMESPACE__4type__5CLASS this, int a)
{
}
int ___9NAMESPACE___5CLASS__8callable__6method(___9NAMESPACE__4type__5CLASS this, int a)
{
    __6vtable___9NAMESPACE__4type__5CLASS vtable = ((void *) this) - 8;
    return (int) (vtable->___9NAMESPACE___5CLASS__8callable__6method)(this, a);
}
void ___9NAMESPACE___5CLASS__8callable__10destructor(___9NAMESPACE__4type__5CLASS this, __6vtable___9NAMESPACE__4type__5CLASS vtable)
{
}
void ___9NAMESPACE___5CLASS__8callable__11constructor(___9NAMESPACE__4type__5CLASS this, __6vtable___9NAMESPACE__4type__5CLASS vtable, int a, char *av)
{
    vtable->___9NAMESPACE___5CLASS__8callable__6method = &___9NAMESPACE___5CLASS__7virtual__6method;
}
___9NAMESPACE__4type__5CLASS ___9NAMESPACE___5CLASS__8callable__6delete(___9NAMESPACE__4type__5CLASS this, __6vtable___9NAMESPACE__4type__5CLASS vtable)
{
    ___9NAMESPACE___5CLASS__8callable__10destructor(this, vtable);
    free(this);
    free(((void *) this - sizeof (void *)));
}
___9NAMESPACE__4type__5CLASS ___9NAMESPACE___5CLASS__8callable__3new(int a, char *av)
{
    ___9NAMESPACE__4type__5CLASS this;
    __6vtable___9NAMESPACE__4type__5CLASS vtable;
    this = sizeof (void *) + malloc(sizeof (void *) + sizeof (*this));
    vtable = ((void *) this) - sizeof (void *);
    vtable = malloc(sizeof (*vtable));
    ___9NAMESPACE___5CLASS__8callable__11constructor(this, vtable, a, av);
    return this;
}
int main()
{
    ___9NAMESPACE__4type__5CLASS var;
    var->___9NAMESPACE___5CLASS__8variable__14test_attribute;
    ;
}

