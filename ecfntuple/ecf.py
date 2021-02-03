"""# submit
htcondor(
    'cmsconnect_blacklist',
    ['*_RU_*', '*FNAL*', '*IFCA*', '*KIPT*', 'T3_IT_Trieste', 'T2_TR_METU', 'T2_US_Vanderbilt', 'T2_PK_NCP']
    )

for mz in [150, 250]:
    for rinv in [0.001, 0.1, 0.3]:
        submit(mz=mz, rinv=rinv)
"""# endsubmit

import qondor, seutils, os.path as osp, os, argparse
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', action='store_true')
args = parser.parse_args()

genfiles = seutils.ls_wildcard(
    'root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/gen/'
    'genjetpt250_Jan25_mz{mz:.0f}_mdark10_rinv{rinv}/*.root'
    .format(mz=qondor.scope.mz, rinv=qondor.scope.rinv)
    )

cmssw = qondor.svj.init_cmssw(
    'root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/svjproduction-tarballs/'
    'CMSSW_10_2_21_efb554a_el7_gen_2018_Feb02_ecfntupler.tar.gz'
    )
rundir = osp.join(cmssw.cmssw_src, 'SVJ/Production/test')


processed_genfiles = []
for i, genfile in enumerate(genfiles):
    if args.test and i == 2: break
    local_rootfile = osp.join(rundir, 'step1.root')
    if osp.isfile(local_rootfile): os.remove(local_rootfile)
    seutils.cp(genfile, local_rootfile)
    cmssw.run_commands([
        'cd {0}'.format(rundir),
        'cmsRun runSVJ.py'
        ' config=genJetSubstructure'
        ' outpre=gensub'
        ' part={i}'
        ' channel=s'
        ' mMediator={mz:.0f}'
        ' mDark=10'
        ' rinv={rinv}'
        ' {maxEvents}'
        .format(
            mz=qondor.scope.mz, rinv=qondor.scope.rinv, i=i+1,
            maxEvents='maxEvents=10' if args.test else ''
            )
        ])
    processed_genfiles.append(
        'gensub_s-channel_mMed-{mz:.0f}_mDark-10_rinv-{rinv}_alpha-peak_13TeV-pythia8_part-{i}.root'
        .format(mz=qondor.scope.mz, rinv=qondor.scope.rinv, i=i+1)
        )

cmssw.run_commands([
    'cd {0}'.format(osp.join(cmssw.cmssw_src, 'SVJ/Production')),
    'cmsRun python/ntuple_gensub.py inputFiles={0}'
    .format(','.join([
        'file:test/' + f for f in processed_genfiles
        ]))
    ])

expected_outfile = osp.join(cmssw.cmssw_src, 'SVJ/Production/flatgensub.root')

if not qondor.BATCHMODE: seutils.drymode()
seutils.cp(
    expected_outfile,
    'root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/boosted/ecfntuples/'
    '{date}_mz{mz:.0f}_rinv{rinv}.root'
    .format(
        date=qondor.get_submission_timestr(),
        mz=qondor.scope.mz,
        rinv=qondor.scope.rinv,
        )
    )
