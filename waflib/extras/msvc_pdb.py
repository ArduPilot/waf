#!/usr/bin/env python
# encoding: utf-8
# Rafaël Kooi 2019

from waflib import TaskGen, Tools
@TaskGen.feature('c', 'cxx', 'fc')
@TaskGen.after_method('propagate_uselib_vars')
def add_pdb_per_object(self):
    """For msvc/fortran, specify a unique compile pdb per object, to work
    around LNK4099. Flags are updated with a unique /Fd flag based on the
    task output name. This is separate from the link pdb.
    """
    if not hasattr(self, 'compiled_tasks'):
        return

    link_task = getattr(self, 'link_task', None)

    for task in self.compiled_tasks:
        node = task.outputs[0].change_ext('.pdb')
        pdb_flag = '/Fd:' + node.abspath()

        canAddNode = False
        for flagname in ('CFLAGS', 'CXXFLAGS', 'FCFLAGS'):
            if not flagname in task.env:
                continue

            flags = task.env[flagname]

            for i, flag in reversed(list(enumerate(flags))):
                # Capture both /Zi and /ZI, which cause the compiler to emit a PDB file.
                if flag[1:].lower() == 'zi':
                    canAddNode = True
                    task.env.append_unique(flagname, pdb_flag)

                # Strip existing /Fd, /FS, or /MP flags.
                # We have to check for /Fd case sensitive, so that we won't accidentally
                # overwrite GCC flags such as "-fdata-sections".
                if flag[1:3] == 'Fd' \
                or flag[1:].lower() == 'fs' \
                or flag[1:].lower() == 'mp':
                    del task.env[flagname][i]

        if canAddNode:
            if link_task and not node in link_task.dep_nodes:
                link_task.dep_nodes.append(node)
            if not node in task.outputs:
                task.outputs.append(node)
