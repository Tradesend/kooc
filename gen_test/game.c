#include <stdlib.h>
#include <stdio.h>
#ifndef ___home_lavrut_f_rendu_kooc_gen_test_game
# define ___home_lavrut_f_rendu_kooc_gen_test_game
# include "/home/lavrut_f/rendu/kooc/gen_test/game.h"
#endif
void ___4game___6weapon__8callable__11constructor(___4game__4type__6weapon this, __6vtable___4game__4type__6weapon vtable)
{
    vtable->___4game___6weapon__8callable__10destructor = &___4game___6weapon__7virtual__10destructor;
    vtable->___4game___6weapon__8callable__3use = &___4game___6weapon__7virtual__3use;
    printf("a weapon has been forged!\n");
}
void ___4game___6weapon__7virtual__10destructor(___4game__4type__6weapon this)
{
    printf("a weapon has been destroyed!\n");
}
void ___4game___6weapon__8callable__10destructor(___4game__4type__6weapon this)
{
    __6vtable___4game__4type__6weapon *vtable = ((void *) this) - 8;
    return (void) ((*vtable)->___4game___6weapon__8callable__10destructor)(this);
}
void ___4game___6weapon__7virtual__3use(___4game__4type__6weapon this)
{
    printf("*generic weapon sound*\n");
}
void ___4game___6weapon__8callable__3use(___4game__4type__6weapon this)
{
    __6vtable___4game__4type__6weapon *vtable = ((void *) this) - 8;
    return (void) ((*vtable)->___4game___6weapon__8callable__3use)(this);
}
___4game__4type__6weapon ___4game___6weapon__8callable__3new()
{
    ___4game__4type__6weapon this;
    __6vtable___4game__4type__6weapon *vtable;
    this = sizeof (void *) + malloc(sizeof (void *) + sizeof (*this));
    vtable = ((void *) this) - sizeof (void *);
    *vtable = malloc(sizeof (**vtable));
    ___4game___6weapon__8callable__11constructor(this, *vtable);
    return this;
}
void ___4game___6weapon__8callable__6delete(___4game__4type__6weapon this)
{
    ___4game___6weapon__8callable__10destructor(this);
    free(this);
    free(((void *) this - sizeof (void *)));
}
void ___4game___4peon__8callable__11constructor(___4game__4type__4peon this, __6vtable___4game__4type__4peon vtable)
{
    vtable->___4game___4peon__8callable__10destructor = &___4game___4peon__7virtual__10destructor;
    vtable->___4game___4peon__8callable__3hit = &___4game___4peon__7virtual__3hit;
    vtable->___4game___4peon__8callable__4talk = &___4game___4peon__7virtual__4talk;
    printf("je suis un peon!\n");
}
void ___4game___4peon__7virtual__10destructor(___4game__4type__4peon this)
{
    printf("je me meurs!\n");
}
void ___4game___4peon__8callable__10destructor(___4game__4type__4peon this)
{
    __6vtable___4game__4type__4peon *vtable = ((void *) this) - 8;
    return (void) ((*vtable)->___4game___4peon__8callable__10destructor)(this);
}
___4game__4type__4peon ___4game___4peon__8callable__3new()
{
    ___4game__4type__4peon this;
    __6vtable___4game__4type__4peon *vtable;
    this = sizeof (void *) + malloc(sizeof (void *) + sizeof (*this));
    vtable = ((void *) this) - sizeof (void *);
    *vtable = malloc(sizeof (**vtable));
    ___4game___4peon__8callable__11constructor(this, *vtable);
    return this;
}
void ___4game___4peon__8callable__6delete(___4game__4type__4peon this)
{
    ___4game___4peon__8callable__10destructor(this);
    free(this);
    free(((void *) this - sizeof (void *)));
}
int main()
{
    ___4game___4peon__8callable__6delete(___4game___4peon__8callable__3new());
}

