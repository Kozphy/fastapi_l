// TODO: wait for stable cmake with gcc c++ 20 modules support.
// Example.ixx
module;
export module Example;

#define ANSWER 42

namespace Example_NS
{
   int f_internal() {
        return ANSWER;
      }

   export int f() {
      return f_internal();
   }
}