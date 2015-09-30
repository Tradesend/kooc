#ifndef demo_h
# define demo_h
#include "demo.h"
#endif

___Geometry__Rectangle* ___Geometry__Rectangle__ctor__int__int__int__int______Geometry__Rectangle__Pointer(int tl1, int tl2, int w, int h) {

  ___Geometry__Rectangle* this = malloc(sizeof(___Geometry__Rectangle));

  this->topLeftCorner = ___Geometry__Point__ctor__int__int______Geometry__Point__Pointer(tl1, tl2);
  this->width = w;
  this->height = h;
  return this;
}
