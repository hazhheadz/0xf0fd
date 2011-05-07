from datastore.dbtypes import *
from datastore.infostore import InfoStore
from datastore import DataStore
import arch


# entry_point is an ident
def codeFollow(ds, arch_name, entry_point):
    from types import FunctionType

    # MAP entry_point to addr - ensure all dests within same seg?
    #                         - run dests thru reverse mapper?

    q = [entry_point]
    arch_info = arch.machineFactory(ds, arch_name)

    while q:
        pc = q.pop()

        rcode, _ = ds.infostore.lookup(pc)

        if rcode != InfoStore.LKUP_NONE:
            print "warning, %s already present, %d" % (pc, rcode)
            continue

        try:
            fetched_mem = ds.readBytes(pc, arch_info.max_length)
        except IOError:
            # If the generated addr is outside of mapped memory, skip it
            continue

        # TODO: HACK: 6 repeated 0xFF's = uninited mem
        if all([i == 0xFF for i in fetched_mem]):
            continue

        segment = ds.segments.findSegment(pc)

        try:
            insn = arch_info.disassemble(pc, None)
        except IOError:
            continue

        # If we can't decode it, leave as is
        if not insn:
            continue

        # Make sure memory is clear
        mem_clear = True
        for i in xrange(1, insn.length()):
            try:
                rc, _ = ds.infostore.lookup(pc + i)
                if rc != InfoStore.LKUP_NONE:
                    mem_clear = False
            except KeyError:
                pass
        if not mem_clear:
            continue

        # HACK - Add destinations, use IR
        try:
            q.extend([segment.mapOut(i) for i, _ in insn.dests()])
        except AttributeError:
            q.extend([insn.length() + pc])

        ds.infostore.setType(pc, arch_name)