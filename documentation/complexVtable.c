#include <stdlib.h>
#include <stdio.h>
#ifndef ___home_lavrut_f_rendu_kooc_test_linear_heritance
# define ___home_lavrut_f_rendu_kooc_test_linear_heritance
# include "/home/lavrut_f/rendu/kooc/test/linear_heritance.h"
#endif
void ___1n___1a__7virtual__10destructor(___1n__4type__1a this)
{
}
void ___1n___1a__8callable__10destructor(___1n__4type__1a this)
{
    __6vtable___1n__4type__1a *vtable = ((void *) this) - 8;
    return (void) ((*vtable)->___1n___1a__8callable__10destructor)(this);
}
void ___1n___1a__8callable__11constructor(___1n__4type__1a this, __6vtable___1n__4type__1a vtable)
{
    vtable->___1n___1a__8callable__10destructor = &___1n___1a__7virtual__10destructor;
}
void ___1n___1a__8callable__6delete(___1n__4type__1a this)
{
    ___1n___1a__8callable__10destructor(this);
    free(this);
    free(((void *) this - sizeof (void *)));
}
___1n__4type__1a ___1n___1a__8callable__3new()
{
    ___1n__4type__1a this;
    __6vtable___1n__4type__1a *vtable;
    this = sizeof (void *) + malloc(sizeof (void *) + sizeof (*this));
    vtable = ((void *) this) - sizeof (void *);
    *vtable = malloc(sizeof (**vtable));
    ___1n___1a__8callable__11constructor(this, *vtable);
    return this;
}
void ___1n___2ap__7virtual__10destructor(___1n__4type__2ap this)
{
}
void ___1n___2ap__8callable__10destructor(___1n__4type__2ap this)
{
    __6vtable___1n__4type__2ap *vtable = ((void *) this) - 8;
    return (void) ((*vtable)->___1n___2ap__8callable__10destructor)(this);
}
void ___1n___2ap__8callable__11constructor(___1n__4type__2ap this, __6vtable___1n__4type__2ap vtable)
{
    vtable->___1n___2ap__8callable__10destructor = &___1n___2ap__7virtual__10destructor;
}
void ___1n___2ap__8callable__6delete(___1n__4type__2ap this)
{
    ___1n___2ap__8callable__10destructor(this);
    free(this);
    free(((void *) this - sizeof (void *)));
}
___1n__4type__2ap ___1n___2ap__8callable__3new()
{
    ___1n__4type__2ap this;
    __6vtable___1n__4type__2ap *vtable;
    this = sizeof (void *) + malloc(sizeof (void *) + sizeof (*this));
    vtable = ((void *) this) - sizeof (void *);
    *vtable = malloc(sizeof (**vtable));
    ___1n___2ap__8callable__11constructor(this, *vtable);
    return this;
}
void ___1n___1b__8callable__11constructor(___1n__4type__1b this, __6vtable___1n__4type__1b vtable)
{
    vtable->___1n___1b__8callable__7methode = &___1n___1b__7virtual__7methode;
    vtable->___1n___1a__8callable__10destructor = &___1n___1b__8callable__10destructor;
    (*(this->__6vtable__1b__2ap))->___1n___2ap__8callable__10destructor = &___1n___1b__8callable__10destructor;
}
void ___1n___1b__8callable__10destructor(___1n__4type__1b this)
{
}
void ___1n___1b__7virtual__7methode(___1n__4type__1b this)
{
    printf("i'm a b\n");
}
void ___1n___1b__8callable__7methode(___1n__4type__1b this)
{
    __6vtable___1n__4type__1b *vtable = ((void *) this) - 8;
    return (void) ((*vtable)->___1n___1b__8callable__7methode)(this);
}
___1n__4type__1b ___1n___1b__8callable__3new()
{
    ___1n__4type__1b this;
    __6vtable___1n__4type__1b *vtable;
    this = sizeof (void *) + malloc(sizeof (void *) + sizeof (*this));
    this->__6vtable__1b__2ap = malloc(sizeof (void *));
    *(this->__6vtable__1b__2ap) = malloc(sizeof (*(this->__6vtable__1b__2ap)));
    vtable = ((void *) this) - sizeof (void *);
    *vtable = malloc(sizeof (**vtable));
    ___1n___1b__8callable__11constructor(this, *vtable);
    return this;
}
void ___1n___1b__8callable__6delete(___1n__4type__1b this)
{
    ___1n___1b__8callable__10destructor(this);
    free(this);
    free(((void *) this - sizeof (void *)));
}
void ___1n___1c__8callable__11constructor(___1n__4type__1c this, __6vtable___1n__4type__1c vtable)
{
    vtable->___1n___1a__8callable__10destructor = &___1n___1c__8callable__10destructor;
    (*(this->__6vtable__1b__2ap))->___1n___2ap__8callable__10destructor = &___1n___1c__8callable__10destructor;
    vtable->___1n___1b__8callable__7methode = &___1n___1c__8callable__7methode;
}
void ___1n___1c__8callable__10destructor(___1n__4type__1c this)
{
}
void ___1n___1c__8callable__7methode(___1n__4type__1c this)
{
    printf("i'm a c\n");
}
___1n__4type__1c ___1n___1c__8callable__3new()
{
    ___1n__4type__1c this;
    __6vtable___1n__4type__1c *vtable;
    this = sizeof (void *) + malloc(sizeof (void *) + sizeof (*this));
    this->__6vtable__1b__2ap = malloc(sizeof (void *));
    *(this->__6vtable__1b__2ap) = malloc(sizeof (*(this->__6vtable__1b__2ap)));
    vtable = ((void *) this) - sizeof (void *);
    *vtable = malloc(sizeof (**vtable));
    ___1n___1c__8callable__11constructor(this, *vtable);
    return this;
}
void ___1n___1c__8callable__6delete(___1n__4type__1c this)
{
    ___1n___1c__8callable__10destructor(this);
    free(this);
    free(((void *) this - sizeof (void *)));
}
int main()
{
    ___1n__4type__1c c_object = ___1n___1c__8callable__3new();
    ___1n__4type__1a a_object = (___1n__4type__1a) c_object;
    c_object->___1n___1a__8variable__1a;
    ;
    ___1n___1b__8callable__7methode((___1n__4type__1b) c_object);
}

