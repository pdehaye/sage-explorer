import inspect
from flask import Flask
from flask import Markup
from flask import render_template

app = Flask(__name__)

@app.route("/<command>")
def hello(command):
  """
  This is responsible for defining object_output (HTML representing the object)
  and optionally object_methods_output (HTML representing methods that can be
  applied to the object).
  """
  sage_output = eval(command)
  # Here we would need a cube-style selector mechanism
  # Runtime type checking for now.
  if isinstance(sage_output, (list, tuple)):
    object_output = Markup(view_list(sage_output, command))
    object_methods_output = None
  else:
    object_output = Markup(view_sage_object(sage_output, command))
    object_methods_output = Markup(view_sage_object_methods(sage_output, command))
  return render_template('template.html', sage_command=command,
      object_output=object_output, object_methods_output=object_methods_output)

def view_list(self, command):
  """
  TODO

  EXAMPLES::

      sage: l = [1,2,3,4]
      sage: view_list(l, "l")
      "[<a href='/l[0]'>1</a>,<a href='/l[1]'>2</a>,<a href='/l[2]'>3</a>,<a href='/l[3]'>4</a>]"
  """
  return "[" + ','.join(url_generator_for_list_item(command, self, i) for i in range(len(self))) + "]"

def url_generator_for_list_item(command, list_object, index):
  return "<a href='/%s[%s]'>%s</a>" % (command, index, list_object[index])

def view_sage_object(self, command):
  """
  TODO
  """
  return "$$" + latex(self) + "$$"

def view_sage_object_methods(self, command):
  return invariants_view(self, command)

def view_element(self):
  pass

def view_parent(self):
  pass

def view_permutation(self):
  pass

def argument_less_methods_of_object(x):
  """
  Returns the list of the names of the methods of ``x`` that take no argument, excluding _methods

  EXAMPLES::

      sage: argument_less_methods_of_object(1)
      ['is_idempotent']
  """
  return [ key for (key, f) in inspect.getmembers(x, inspect.ismethod) if len(inspect.getargspec(f).args)==1 and not key[0] == "_"]

def invariants_view(self, command):
    """
    EXAMPLES::

        sage: print invariants_view(Permutation([2,1]), "foo")
        <ul>
        <li><a href='/foo.bruhat_greater()'>bruhat_greater</a>
        <li><a href='/foo.bruhat_inversions()'>bruhat_inversions</a>
        ...
        </ul>
    """
    invariants = argument_less_methods_of_object(self)
    return "<ul>" + " ".join("<li>" + url_generator_for_invariant(invariant, command) for invariant in invariants) + "</ul>"

def url_generator_for_invariant(invariant, command):
  return "<a href='/%s.%s()'>%s</a>" % (command, invariant, invariant)

# Stupid test that we are not running within Sage
if not "Permutations" in globals():
  from sage.all import *
  if __name__ == "__main__":
    app.run(debug=True)
