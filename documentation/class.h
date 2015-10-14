typedef struct ___6struct__5Point__ ___6struct__5Point__
typedef struct ___6struct__9Rectangle__ ___6struct__9Rectangle__
typedef struct ___6struct__5Carre__ ___6struct__5Carre__

struct ___6struct__5Point__
{ . . . };

struct ___6struct__9Rectangle__ {
  ___6struct__5Point__* topLeftCorner;
  int width;
  int height;
};

struct ___6struct__5Carre__ {
  ___6struct__9Rectangle__ ___Geometry__Rectangle__super;
};

___6struct__9Rectangle__* ___9Rectangle__8function__4ctor__3int__3int__3int__3int__
                          30___6struct__9Rectangle_Pointer____(int, int, int, int);
___6struct__9Rectangle__* ___9Rectangle__8function__4ctor__20___6struct__5Point__
                          __3int__3int__32___6struct__9Rectangle_Pointer__(Point, int, int);
void ___9Rectangle__8function__4dtor__4void__(___6struct__9Rectangle__ *);
___6struct__5Point__* ___24___6struct__9Rectangle____8function__
                      10findMiddle__20___6struct__5Point__(___6struct__9Rectangle__ *);

___6struct__5Carre__* ___19__6struct__5Carre__ __8function__4ctor__3int__3int__3int__
                      28___6struct__5Carre_Pointer__(___6struct__5Carre__ *);
