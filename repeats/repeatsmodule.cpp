#include <Python.h>
#include "repeats.h"

static PyObject *RepeatsError;

static PyObject *repeats_supermax(PyObject *self, PyObject *args)
{
    (void)self;

    const char *command;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;

    std::vector<REPEAT> repeats = supermax(command);

    PyObject* list = PyList_New(PyLong_AsSsize_t(PyLong_FromLong(0)));
    for(unsigned long i = 0; i < repeats.size(); i++) {
        PyObject* occur = PyList_New(PyLong_AsSsize_t(PyLong_FromLong(0)));
        for(unsigned long j = 0; j < repeats[i].occur.size(); j++) {
            PyList_Append(occur, PyLong_FromLong((long)repeats[i].occur[j]));
        }

        PyList_Append(list, occur);
        PyList_Append(list, PyLong_FromLong((long)repeats[i].length));
        PyList_Append(list, PyUnicode_FromString(repeats[i].sequence.c_str()));
    }

    return list;
}

static PyMethodDef RepeatsMethods[] = {
    {"supermax",  repeats_supermax, METH_VARARGS,
     "Find location and values of super maximal repeats in given string."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef repeatsmodule = {
    PyModuleDef_HEAD_INIT,
    "repeats",   /* name of module */
    NULL,     /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    RepeatsMethods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC PyInit_repeats(void)
{
    PyObject *m;

    m = PyModule_Create(&repeatsmodule);
    if (m == NULL)
        return NULL;

    RepeatsError = PyErr_NewException("repeats.error", NULL, NULL);
    Py_INCREF(RepeatsError);
    PyModule_AddObject(m, "error", RepeatsError);
    return m;
}


int main(int argc, char *argv[])
{
    (void)argc;

    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }

    /* Add a built-in module, before Py_Initialize */
    PyImport_AppendInittab("repeats", PyInit_repeats);

    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(program);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Optionally import the module; alternatively,
       import can be deferred until the embedded script
       imports it. */
    PyImport_ImportModule("repeats");

    PyMem_RawFree(program);
    return 0;
}
