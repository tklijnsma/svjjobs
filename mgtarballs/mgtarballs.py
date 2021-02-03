"""# submit
htcondor('request_memory', '4096MB')

htcondor(
    'cmsconnect_blacklist',
    ['*_RU_*', '*FNAL*', '*IFCA*', '*KIPT*', 'T3_IT_Trieste', 'T2_TR_METU', 'T2_US_Vanderbilt', 'T2_PK_NCP']
    )

for mz in [150, 250, 450, 650]:
    for rinv in [ 0.001, 0.1, 0.3, 0.5 ]:
        submit(mz=mz, mdark=10., rinv=rinv)
"""# endsubmit

import qondor, seutils, os.path as osp

cmssw = qondor.svj.init_cmssw('root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/svjproduction-tarballs/CMSSW_10_2_21_latest_el7_gen_2018.tar.gz')

physics = qondor.svj.Physics({
    'year' : 2018,
    'mz' : qondor.scope.mz,
    'mdark' : qondor.scope.mdark,
    'rinv' : qondor.scope.rinv,
    'max_events' : 1,
    })

expected_outfile = cmssw.make_madgraph_tarball(physics)

if not qondor.BATCHMODE: seutils.drymode()
dst = osp.join(
    'root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/mg_tarballs_2021',
    osp.basename(expected_outfile)
    )
seutils.cp(expected_outfile, dst)
