"""# submit
htcondor(
    'cmsconnect_blacklist',
    ['*_RU_*', '*FNAL*', '*IFCA*', '*KIPT*', 'T3_IT_Trieste', 'T2_TR_METU', 'T2_US_Vanderbilt', 'T2_PK_NCP']
    )

for mz in [150, 250]:
    for i in range(1,41):
        for rinv in [0.001, 0.1, 0.3]:
            submit(i=i, mz=mz, mdark=10., rinv=rinv)
"""# endsubmit

import qondor, seutils, os.path as osp

cmssw = qondor.svj.init_cmssw(
    'root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/svjproduction-tarballs/CMSSW_10_2_21_latest_el7_gen_2018.tar.gz'
    )

physics = qondor.svj.Physics({
    'year' : 2018,
    'mz' : qondor.scope.mz,
    'mdark' : qondor.scope.mdark,
    'rinv' : qondor.scope.rinv,
    'mingenjetpt' : 250.,
    'max_events' : 30000,
    'part' : qondor.scope.i
    })

cmssw.download_madgraph_tarball(physics)
expected_outfile = cmssw.run_step('step0_GRIDPACK', 'step1_LHE-GEN', physics)

if not qondor.BATCHMODE: seutils.drymode()
seutils.cp(
    expected_outfile,
    'root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/gen/'
    'genjetpt250_{date}_mz{mz:.0f}_mdark{mdark:.0f}_rinv{rinv}/{i}.root'
    .format(
        date = qondor.get_submission_timestr(),
        i = qondor.scope.i,
        **physics
        )
    )
