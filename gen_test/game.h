#include <stdlib.h>
typedef struct ___4game__5class__6weapon *___4game__4type__6weapon;
typedef struct __6vtable___4game__5class__6weapon *__6vtable___4game__4type__6weapon;
void ___4game___6weapon__8callable__11constructor(___4game__4type__6weapon, __6vtable___4game__4type__6weapon);
___4game__4type__6weapon ___4game___6weapon__8callable__3new();
void ___4game___6weapon__7virtual__10destructor(___4game__4type__6weapon);
void ___4game___6weapon__8callable__10destructor(___4game__4type__6weapon);
void ___4game___6weapon__8callable__6delete(___4game__4type__6weapon);
void ___4game___6weapon__7virtual__3use(___4game__4type__6weapon);
void ___4game___6weapon__8callable__3use(___4game__4type__6weapon);
struct __attribute__((packed))  __6vtable___4game__5class__6weapon {
    void (*___4game___6weapon__8callable__10destructor)(___4game__4type__6weapon);
    void (*___4game___6weapon__8callable__3use)(___4game__4type__6weapon);
    };
struct __attribute__((packed))  ___4game__5class__6weapon {
    };
typedef struct ___4game__5class__5sword *___4game__4type__5sword;
typedef struct __6vtable___4game__5class__5sword *__6vtable___4game__4type__5sword;
void ___4game___5sword__8callable__11constructor(___4game__4type__5sword, __6vtable___4game__4type__5sword);
___4game__4type__5sword ___4game___5sword__8callable__3new();
void ___4game___5sword__8callable__10destructor(___4game__4type__5sword);
void ___4game___5sword__8callable__6delete(___4game__4type__5sword);
void ___4game___5sword__8callable__3use(___4game__4type__5sword);
struct __attribute__((packed))  __6vtable___4game__5class__5sword {
    void (*___4game___6weapon__8callable__10destructor)(___4game__4type__5sword);
    void (*___4game___6weapon__8callable__3use)(___4game__4type__5sword);
    };
struct __attribute__((packed))  ___4game__5class__5sword {
    };
typedef struct ___4game__5class__6dagger *___4game__4type__6dagger;
typedef struct __6vtable___4game__5class__6dagger *__6vtable___4game__4type__6dagger;
void ___4game___6dagger__8callable__11constructor(___4game__4type__6dagger, __6vtable___4game__4type__6dagger);
___4game__4type__6dagger ___4game___6dagger__8callable__3new();
void ___4game___6dagger__8callable__10destructor(___4game__4type__6dagger);
void ___4game___6dagger__8callable__6delete(___4game__4type__6dagger);
void ___4game___6dagger__8callable__3use(___4game__4type__6dagger);
struct __attribute__((packed))  __6vtable___4game__5class__6dagger {
    void (*___4game___6weapon__8callable__10destructor)(___4game__4type__6dagger);
    void (*___4game___6weapon__8callable__3use)(___4game__4type__6dagger);
    };
struct __attribute__((packed))  ___4game__5class__6dagger {
    };
typedef struct ___4game__5class__4peon *___4game__4type__4peon;
typedef struct __6vtable___4game__5class__4peon *__6vtable___4game__4type__4peon;
void ___4game___4peon__8callable__11constructor(___4game__4type__4peon, __6vtable___4game__4type__4peon);
___4game__4type__4peon ___4game___4peon__8callable__3new();
void ___4game___4peon__7virtual__10destructor(___4game__4type__4peon);
void ___4game___4peon__8callable__10destructor(___4game__4type__4peon);
void ___4game___4peon__8callable__6delete(___4game__4type__4peon);
void ___4game___4peon__8callable__10set_weapon(___4game__4type__4peon, ___4game__4type__6weapon);
void ___4game___4peon__7virtual__3hit(___4game__4type__4peon, const char *target);
void ___4game___4peon__8callable__3hit(___4game__4type__4peon, const char *target);
void ___4game___4peon__7virtual__4talk(___4game__4type__4peon);
void ___4game___4peon__8callable__4talk(___4game__4type__4peon);
struct __attribute__((packed))  __6vtable___4game__5class__4peon {
    void (*___4game___4peon__8callable__10destructor)(___4game__4type__4peon);
    void (*___4game___4peon__8callable__3hit)(___4game__4type__4peon, const char *target);
    void (*___4game___4peon__8callable__4talk)(___4game__4type__4peon);
    };
struct __attribute__((packed))  ___4game__5class__4peon {
    ___4game__4type__6weapon ___4game___4peon__8variable__6weapon;
    };
typedef struct ___4game__5class__7warrior *___4game__4type__7warrior;
typedef struct __6vtable___4game__5class__7warrior *__6vtable___4game__4type__7warrior;
void ___4game___7warrior__8callable__11constructor(___4game__4type__7warrior, __6vtable___4game__4type__7warrior);
___4game__4type__7warrior ___4game___7warrior__8callable__3new();
void ___4game___7warrior__8callable__10destructor(___4game__4type__7warrior);
void ___4game___7warrior__8callable__6delete(___4game__4type__7warrior);
void ___4game___7warrior__8callable__3hit(___4game__4type__7warrior, const char *target);
void ___4game___7warrior__8callable__4talk(___4game__4type__7warrior);
struct __attribute__((packed))  __6vtable___4game__5class__7warrior {
    void (*___4game___4peon__8callable__10destructor)(___4game__4type__7warrior);
    void (*___4game___4peon__8callable__3hit)(___4game__4type__7warrior, const char *target);
    void (*___4game___4peon__8callable__4talk)(___4game__4type__7warrior);
    };
struct __attribute__((packed))  ___4game__5class__7warrior {
    ___4game__4type__6weapon ___4game___4peon__8variable__6weapon;
    };
typedef struct ___4game__5class__5rogue *___4game__4type__5rogue;
typedef struct __6vtable___4game__5class__5rogue *__6vtable___4game__4type__5rogue;
void ___4game___5rogue__8callable__11constructor(___4game__4type__5rogue, __6vtable___4game__4type__5rogue);
___4game__4type__5rogue ___4game___5rogue__8callable__3new();
void ___4game___5rogue__8callable__10destructor(___4game__4type__5rogue);
void ___4game___5rogue__8callable__6delete(___4game__4type__5rogue);
void ___4game___5rogue__8callable__3hit(___4game__4type__5rogue, const char *target);
void ___4game___5rogue__8callable__4talk(___4game__4type__5rogue);
struct __attribute__((packed))  __6vtable___4game__5class__5rogue {
    void (*___4game___4peon__8callable__10destructor)(___4game__4type__5rogue);
    void (*___4game___4peon__8callable__3hit)(___4game__4type__5rogue, const char *target);
    void (*___4game___4peon__8callable__4talk)(___4game__4type__5rogue);
    };
struct __attribute__((packed))  ___4game__5class__5rogue {
    ___4game__4type__6weapon ___4game___4peon__8variable__6weapon;
    };

