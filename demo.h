/*
** demo.h for demo in /home/moran-_d/rendu/kooc
** 
** Made by moran-_d
** Login   <moran-_d@epitech.net>
** 
** Started on  Wed Sep 30 13:12:16 2015 moran-_d
** Last update Wed Sep 30 15:05:08 2015 moran-_d
*/

/*
** DEFINITIONS CLASSES
*/

typedef struct ___struct__Geometry__Rectangle ___Geometry__Rectangle__
typedef struct ___struct__Geometry__Carre ___Geometry__Carre__

struct ___struct__Geometry__Rectangle
{
  ___Geometry__Point__* topLeftCorner;
  int width;
  int height;
};

struct ___struct__Geometry__Carre
{
  ___Geometry__Rectangle ___Geometry__Rectangle__super;
};

/*
*** DEFINITIONS FONCTIONS
*/

/* ___Geometry__Rectangle */
___Geometry__Rectangle* ___Geometry__Rectangle__Function__ctor__int__int__int__int___Rectangle__Pointer(int, int, int, int);
___Geometry__Rectangle* ___Geometry__Rectangle__Function__ctor_____Geometry__Point__Pointer__int__int___RectanglePtr(___Geometry__Point *, int, int);
void ___Geometry__Rectangle__Function__dtor___void();
___Geometry__Point* ___Geometry__Rectangle__Function__findMiddle______Geometry__Point__Pointer(___Geometry__Rectangle*);

/* ___Geometry__Carre */
___Geometry__Carre* ___Geometry__Carre__Function__ctor__int__int__int______Geometry__Carre__Pointer(int, int, int);
