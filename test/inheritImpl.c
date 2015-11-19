#include <stdlib.h>
#ifndef ___home_lavrut_f_rendu_kooc_test_inheritence
# define ___home_lavrut_f_rendu_kooc_test_inheritence
# include "/home/lavrut_f/rendu/kooc/test/inheritence.h"
#endif
int ___9NAMESPACE___5CLASS__8callable__6method(___9NAMESPACE__4type__5CLASS this, int a)
{
}
void ___9NAMESPACE___5CLASS__8callable__11constructor(___9NAMESPACE__4type__5CLASS this, __6vtable___9NAMESPACE__4type__5CLASS vtable, int a, char *av)
{
    vtable->___9NAMESPACE___5SUPER__8callable__6method = &___9NAMESPACE___5CLASS__8callable__6method;
}
___9NAMESPACE__4type__5CLASS ___9NAMESPACE___5CLASS__8callable__3new(int a, char *av)
{
    ___9NAMESPACE__4type__5CLASS this;
    __6vtable___9NAMESPACE__4type__5CLASS *vtable;
    this = sizeof (void *) + malloc(sizeof (void *) + sizeof (*this));
    vtable = ((void *) this) - sizeof (void *);
    *vtable = malloc(sizeof (**vtable));
    ___9NAMESPACE___5CLASS__8callable__11constructor(this, *vtable, a, av);
    return this;
}
int main()
{
    ___9NAMESPACE__4type__5CLASS c = ___9NAMESPACE___5CLASS__8callable__3new(45, "toto");
    int a = ___9NAMESPACE___5CLASS__8callable__6method((___9NAMESPACE__4type__5CLASS) c, 10);
}

