"""
#;+ 
#; NAME:
#; voigt
#;    Version 1.0
#;
#; PURPOSE:
#;    Module for Voigt profiles
#;   01-Nov-2014 by JXP
#;      ## Heavily adapted from Ryan Cooke (e.g. alis)
#;-
#;------------------------------------------------------------------------------
"""
from __future__ import print_function, absolute_import, division, unicode_literals

import numpy as np
import sys
import os
import copy
import warnings

from astropy import units as u
from astropy.units import Unit, Quantity
from astropy import constants as const
from astropy.modeling import FittableModel, Parameter

from linetools.spectra.xspectrum1d import XSpectrum1D
from linetools.spectralline import AbsLine

#from xastropy.xutils import xdebug as xdb

# The standard King model
def voigtking(vin,a):
    oneonsqrtpi=0.56418958354775630
    h0 = np.array([ 1.0e0, 0.9975031223974601240368798e0, 0.9900498337491680535739060e0, 0.9777512371933363639286036e0, 0.9607894391523232094392107e0, 0.9394130628134757861197108e0, 0.9139311852712281867473535e0, 0.8847059049434835594929548e0, 0.8521437889662113384563470e0, 0.8166864825981108401538061e0, 0.7788007830714048682451703e0, 0.7389684882589442416058206e0, 0.6976763260710310572091293e0, 0.6554062543268405127576690e0, 0.6126263941844160689885800e0, 0.5697828247309230097666297e0, 0.5272924240430485572436946e0, 0.4855368951540794399916001e0, 0.4448580662229411344814454e0, 0.4055545050633205516443034e0, 0.3678794411714423215955238e0, 0.3320399453446606420249195e0, 0.2981972794298873779316010e0, 0.2664682978135241116965901e0, 0.2369277586821217567233665e0, 0.2096113871510978225241101e0, 0.1845195239929892676298138e0, 0.1616211924653392539324509e0, 0.1408584209210449961479715e0, 0.1221506695399900084151679e0, 0.1053992245618643367832177e0, 0.9049144166369591062935159e-1, 0.7730474044329974599046566e-1, 0.6571027322750286139200605e-1, 0.5557621261148306865356766e-1, 0.4677062238395898365276137e-1, 0.3916389509898707373977109e-1, 0.3263075599289603180381419e-1, 0.2705184686635041108596167e-1, 0.2231491477696640649487920e-1, 0.1831563888873418029371802e-1, 0.1495813470057748930092482e-1, 0.1215517832991493721502629e-1, 0.9828194835379685936011149e-2, 0.7907054051593440493635646e-2, 0.6329715427485746576865117e-2, 0.5041760259690979102410257e-2, 0.3995845830084632413030896e-2, 0.3151111598444440557819106e-2, 0.2472563035874193226953048e-2, 0.1930454136227709242213512e-2, 0.1499685289329846120368399e-2, 0.1159229173904591150012118e-2, 0.8915937199952195568639939e-3, 0.6823280527563766163014506e-3, 0.5195746821548384817648154e-3, 0.3936690406550782109805393e-3, 0.2967857677932108344855019e-3, 0.2226298569188890101840659e-3, 0.1661698666072774484528398e-3, 0.1234098040866795494976367e-3, 0.9119595636226606575873788e-4, 0.6705482430281108867614262e-4, 0.4905835745620769579106241e-4, 0.3571284964163521691234528e-4, 0.2586810022265412127035909e-4, 0.1864374233151683041526522e-4, 0.1336996212084380475632834e-4, 0.9540162873079234841590110e-5, 0.6773449997703748098370991e-5, 0.4785117392129009089609771e-5, 0.3363595724825637829225185e-5, 0.2352575200009772922652510e-5, 0.1637237807196195233271403e-5, 0.1133727138747965652009438e-5, 0.7811489408304490795473004e-6, 0.5355347802793106157479094e-6, 0.3653171341207511214363159e-6, 0.2479596018045029629499234e-6, 0.1674635703137489046698250e-6, 0.1125351747192591145137752e-6, 0.7524623257644829651017174e-7, 0.5006218020767042215644986e-7, 0.3314082270898834287088712e-7, 0.2182957795125479209083827e-7, 0.1430724191856768833467676e-7, 0.9330287574504991120387842e-8, 0.6054282282484886644264747e-8, 0.3908938434264861859681131e-8, 0.2511212833271291589987176e-8, 0.1605228055185611608653934e-8, 0.1020982947159334870301705e-8, 0.6461431773106108989429857e-9, 0.4068811450655793356678124e-9, 0.2549381880391968872012880e-9, 0.1589391009451636652873474e-9, 0.9859505575991508240729766e-10, 0.6085665105518337082108266e-10, 0.3737571327944262032923964e-10, 0.2284017657993705413027994e-10, 0.1388794386496402059466176e-10, 0.8402431396484308187150245e-11, 0.5058252742843793235026422e-11, 0.3029874246723653849216172e-11, 0.1805831437513215621913785e-11, 0.1070923238250807645586450e-11, 0.6319285885175366663984108e-12, 0.3710275783094727281418983e-12, 0.2167568882618961942307398e-12, 0.1259993054847742150188394e-12, 0.7287724095819692419343177e-13, 0.4194152536192217185131208e-13, 0.2401734781620959445230543e-13, 0.1368467228126496785536523e-13, 0.7758402075696070467242451e-14, 0.4376618502870849893821267e-14, 0.2456595368792144453705261e-14, 0.1372009419645128473380053e-14, 0.7624459905389739760616425e-15, 0.4215893238174252040735029e-15, 0.2319522830243569388312264e-15, 0.1269802641377875575018264e-15, 0.6916753975541448863883054e-16, 0.3748840457745443581785685e-16, 0.2021715848695342027119482e-16, 0.1084855264042937802512215e-16, 0.5792312885394857923477507e-17, 0.3077235638152508657901574e-17, 0.1626664621453244338034305e-17, 0.8555862896902856300749061e-18, 0.4477732441718301199042103e-18, 0.2331744656246116743545942e-18, 0.1208182019899973571654094e-18, 0.6228913128535643653088166e-19, 0.3195366717748344275120932e-19, 0.1631013922670185678641901e-19, 0.8283677007682876110228791e-20, 0.4186173006145967657832773e-20, 0.2104939978339734445589080e-20, 0.1053151347744013743766989e-20, 0.5242885663363463937171805e-21, 0.2597039249246848208769072e-21, 0.1280015319051641983953037e-21, 0.6277407889747195099574399e-22, 0.3063190864577440373821128e-22, 0.1487292181651270619154227e-22, 0.7185335635902193010046941e-23, 0.3454031957013868448981675e-23, 0.1652091782314268593068387e-23, 0.7862678502984538622254116e-24, 0.3723363121750510429289070e-24, 0.1754400713566556605465117e-24, 0.8225280651606668501925640e-25, 0.3837082905344536379879530e-25, 0.1781066634757091357021587e-25, 0.8225980595143903024275237e-26, 0.3780277844776084635218009e-26, 0.1728575244037268289032505e-26, 0.7864685935766448441713277e-27, 0.3560434556451067378310069e-27, 0.1603810890548637852976087e-27, 0.7188393394953158727447087e-28, 0.3205819323394999444158648e-28, 0.1422573701362478490703169e-28, 0.6281148147605989215436687e-29, 0.2759509067522042024589005e-29, 0.1206293927781149203841840e-29, 0.5246902396795390138796640e-30, 0.2270812922026396509517690e-30, 0.9778860615814667663870901e-31, 0.4190093194494397377123780e-31, 0.1786436718517518413888050e-31, 0.7578445267618382646037748e-32, 0.3198903416725805416294188e-32, 0.1343540197758737662452134e-32, 0.5614728092387934579799402e-33, 0.2334722783487267408869808e-33, 0.9659851300583384710233199e-34, 0.3976803097901655265751816e-34, 0.1629019426220514693169818e-34, 0.6639677199580734400702255e-35, 0.2692751000456178970430831e-35, 0.1086610640745980532852592e-35, 0.4362950029268711046345153e-36, 0.1743070896645292498913954e-36, 0.6929124938815710000577778e-37, 0.2740755284722598699701951e-37, 0.1078675105373929991550997e-37, 0.4224152406206200437573993e-38, 0.1645951484063258284098658e-38, 0.6381503448060790393554118e-39, 0.2461826907787885454919214e-39, 0.9449754976491185028813549e-40, 0.3609209642415355020302235e-40, 0.1371614910949353618952282e-40, 0.5186576811908572940413120e-41, 0.1951452380295377748121319e-41, 0.7305730197111493885868359e-42, 0.2721434140093713884466599e-42, 0.1008696596314342558322441e-42, 0.3720075976020835962959696e-43, 0.1365122395620087240477630e-43 ], dtype=np.float64)
    h1 = np.array([ -1.128379167095512573896159e0, -1.122746665023313894112994e0, -1.105961434222613497822717e0, -1.078356949458362356972974e0, -1.040477963566390226869037e0, -0.9930644092865188274925694e0, -0.9370297574325730524254160e0, -0.8734346738611667009559691e0, -0.8034569860177944012914767e0, -0.7283590897795191457635390e0, -0.6494539941944691013512214e0, -0.5680712138345335512208471e0, -0.4855236771153186839197872e0, -0.4030767281964792012404736e0, -0.3219201665209207840831093e0, -0.2431441002236951675148354e0, -0.1677191974661332963609891e0, -0.9648171389061105293546881e-1, -0.3012346558870770535102483e-1, 0.3081328457047809980986685e-1, 0.8593624458727488433391777e-1, 0.1349991935349749351748713e0, 0.1778942744880748462232135e0, 0.2146410885736963723412265e0, 0.2453732617833523433216744e0, 0.2703231847626659615037426e0, 0.2898056218155761132507312e0, 0.3042008523837261147222841e0, 0.3139379509747736418513567e0, 0.3194787353320834397089635e0, 0.3213028233267945998845488e0, 0.3198941423604233541674753e0, 0.3157291364070343763776039e0, 0.3092668200208504802085382e0, 0.3009407397271468294117335e0, 0.2911528243392948676821857e0, 0.2802690390913659378360681e0, 0.2686167052981096351368975e0, 0.2564833079412283848897372e0, 0.2441165877658165024921633e0, 0.2317257011687522312257119e0, 0.2194832289213470945135105e0, 0.2075278218310246553881156e0, 0.1959672858880207128215797e0, 0.1848819293094190730287360e0, 0.1743280173110208640535652e0, 0.1643412057011470302647273e0, 0.1549398500207542791790132e0, 0.1461281117364874603340094e0, 0.1378988059908943461128856e0, 0.1302359559637753421977543e0, 0.1231170365911391556632533e0, 0.1165149050377156668055896e0, 0.1103994269264874144398788e0, 0.1047388160423518894772002e0, 0.9950071130235648759030670e-1, 0.9465301854781620910441970e-1, 0.9016454652735125189272609e-1, 0.8600546667768981700419079e-1, 0.8214762533231104047151097e-1, 0.7856473513008974607178765e-1, 0.7523246995193424459351750e-1, 0.7212848493340500348466924e-1, 0.6923238018945846374255513e-1, 0.6652562400245432725286132e-1, 0.6399144848312167544450556e-1, 0.6161472819590847810012464e-1, 0.5938184999317344054777048e-1, 0.5728058034957269600588669e-1, 0.5529993483145627029203620e-1, 0.5343005296426139233134751e-1, 0.5166208065197234887486323e-1, 0.4998806142885727821214551e-1, 0.4840083715410895783485349e-1, 0.4689395826338997495993764e-1, 0.4546160333748704598916335e-1, 0.4409850750954268216573793e-1, 0.4279989908392569899980027e-1, 0.4156144366035708515282858e-1, 0.4037919502845779134315796e-1, 0.3924955210570969222557380e-1, 0.3816922122416471946490538e-1, 0.3713518311895684989765586e-1, 0.3614466402785612590311943e-1, 0.3519511037069617482332004e-1, 0.3428416653694949866994660e-1, 0.3340965536664229903158673e-1, 0.3256956096272257612903376e-1, 0.3176201352112533673779090e-1, 0.3098527590780517228496903e-1, 0.3023773174995156695256252e-1, 0.2951787484170619418302355e-1, 0.2882429969333463230632146e-1, 0.2815569307740452259166926e-1, 0.2751082644654734935368337e-1, 0.2688854911528297388431485e-1, 0.2628778211358937241904422e-1, 0.2570751263279204975253415e-1, 0.2514678899527364475073049e-1, 0.2460471608876676259183765e-1, 0.2408045121385331090696902e-1, 0.2357320029997478838776359e-1, 0.2308221445094914570064896e-1, 0.2260678678585010840991674e-1, 0.2214624954526743636682309e-1, 0.2169997143654264861646818e-1, 0.2126735519465680897241377e-1, 0.2084783533811200664569883e-1, 0.2044087610146017752978434e-1, 0.2004596952814515567227767e-1, 0.1966263370908071277476715e-1, 0.1929041115392591487587378e-1, 0.1892886728337045173071115e-1, 0.1857758903193275942486415e-1, 0.1823618355182474294515453e-1, 0.1790427700936730343669473e-1, 0.1758151346626646308038721e-1, 0.1726755383879409857500321e-1, 0.1696207492857163038741910e-1, 0.1666476851923932358834102e-1, 0.1637534053381661837450139e-1, 0.1609351024802744708797459e-1, 0.1581900955528515170398058e-1, 0.1555158227940989996039230e-1, 0.1529098353149220739767610e-1, 0.1503697910762349625920090e-1, 0.1478934492449222808347731e-1, 0.1454786649009525295887101e-1, 0.1431233840704145462214254e-1, 0.1408256390613103046576229e-1, 0.1385835440808103075999097e-1, 0.1363952911143803959964144e-1, 0.1342591460487383719630737e-1, 0.1321734450220107129175951e-1, 0.1301365909857474699723209e-1, 0.1281470504646293252049926e-1, 0.1262033505007755515762735e-1, 0.1243040757705449418533892e-1, 0.1224478658626222948827240e-1, 0.1206334127070085131071308e-1, 0.1188594581452897199141430e-1, 0.1171247916332562864755594e-1, 0.1154282480675818732553606e-1, 0.1137687057288605896976939e-1, 0.1121450843338417065773542e-1, 0.1105563431902001242285305e-1, 0.1090014794476407143162512e-1, 0.1074795264395590657657700e-1, 0.1059895521098731117021612e-1, 0.1045306575200023435008377e-1, 0.1031019754313063242129945e-1, 0.1017026689586042607609242e-1, 0.1003319302906845397201302e-1, 0.9898897947397924639729408e-2, 0.9767306325582547468180475e-2, 0.9638345398396424782187982e-2, 0.9511944855914052317394595e-2, 0.9388036743786533882143785e-2, 0.9266555368258485665416943e-2, 0.9147437205667194364984339e-2, 0.9030620816181499749829423e-2, 0.8916046761552686783940876e-2, 0.8803657526663477808232965e-2, 0.8693397444674087410976982e-2, 0.8585212625576311168220303e-2, 0.8479050887977828363904268e-2, 0.8374861693949366877024963e-2, 0.8272596086777159693185345e-2, 0.8172206631472266686907249e-2, 0.8073647357896888215194357e-2, 0.7976873706375800846399120e-2, 0.7881842475668539112571351e-2, 0.7788511773184966394916599e-2, 0.7696840967333456047851643e-2, 0.7606790641897071224649652e-2, 0.7518322552338916854888971e-2, 0.7431399583943265980411531e-2, 0.7345985711704159367477213e-2, 0.7262045961877964368036759e-2, 0.7179546375120877141317720e-2, 0.7098453971136580788416864e-2, 0.7018736714763248519923831e-2, 0.6940363483432822204243367e-2, 0.6863304035939017881037086e-2, 0.6787528982453825324020280e-2, 0.6713009755735391745310971e-2, 0.6639718583473122562606414e-2, 0.6567628461718606252976457e-2, 0.6496713129353586350126915e-2, 0.6426947043548671526978323e-2, 0.6358305356168803683625031e-2, 0.6290763891083702643557758e-2, 0.6224299122343582476647260e-2, 0.6158888153182396103862750e-2, 0.6094508695812718682782931e-2, 0.6031139051978132847456608e-2, 0.5968758094230636272231571e-2, 0.5907345247902159938278185e-2, 0.5846880473740769223255677e-2, 0.5787344251183524483318654e-2, 0.5728717562239307805652498e-2, 0.5670981875956182433959706e-2 ], dtype=np.float64)
    h2 = np.array([ 1.0e0, 0.9925156067854728234166954e0, 0.9702488370741846925024279e0, 0.9337524315196362275518164e0, 0.8839262840201373526840738e0, 0.8219864299617913128547470e0, 0.7494235719224071131328299e0, 0.6679529582323300874171809e0, 0.5794577764970237101503160e0, 0.4859284571458759498915146e0, 0.3894003915357024341225852e0, 0.2918925528622829754342991e0, 0.1953493712998886960185562e0, 0.1015879694206602794774387e0, 0.1225252788368832137977160e-1, -0.7122285309136537622082871e-1, -0.1476418787320535960282345e0, -0.2160639183435653507962620e0, -0.2758120010582235033784961e0, -0.3264713765759730440736642e0, -0.3678794411714423215955238e0, -0.4001081341403160736400280e0, -0.4234401367904400766628734e0, -0.4383403499032471637408907e0, -0.4454241863223889026399290e0, -0.4454241976960828728637340e0, -0.4391564671033144569589568e0, -0.4274880540708223266513326e0, -0.4113065890894513887520768e0, -0.3914928958756679769706131e0, -0.3688972859665251787412620e0, -0.3443199355303629399446828e0, -0.3184955306263949534807185e0, -0.2920821644962502188874669e0, -0.2656542962828890681640534e0, -0.2396994397177897912204020e0, -0.2146181451424491640939456e0, -0.1907267687784773058932939e0, -0.1682624875086995569546816e0, -0.1473900121018631148986771e0, -0.1282094722211392620560261e0, -0.1107649874577763082733483e0, -0.9505349453993480902150559e-1, -0.8103346641770551054241192e-1, -0.6863322916783106348475741e-1, -0.5775865327580743751389419e-1, -0.4830006328783957980109026e-1, -0.4013827136320013258889535e-1, -0.3314969401563551466825700e-1, -0.2721055620979549646261829e-1, -0.2220022256661865628545539e-1, -0.1800372189840480267502263e-1, -0.1451354925728548119815172e-1, -0.1163084007733763911929080e-1, -0.9266014956431594449373699e-2, -0.7338992385437093554928018e-2, -0.5779061516816548137194317e-2, -0.4524499030007499171731476e-2, -0.3522004336456824141111923e-2, -0.2726016661692386541868837e-2, -0.2097966669473552341459824e-2, -0.1605504811757694087682580e-2, -0.1221738898797218035679319e-2, -0.9245047462622340271825711e-3, -0.6956863110190540254524861e-3, -0.5205955169809141905659767e-3, -0.3874169656489197360292113e-3, -0.2867188376814953929994613e-3, -0.2110284027525126746959732e-3, -0.1544685271976339753833504e-3, -0.1124502587150317136058296e-3, -0.8141583451940456365639560e-4, -0.5862617398424354123250055e-4, -0.4198696356554642675724513e-4, -0.2990772192017133390000897e-4, -0.2118866502002593128272052e-4, -0.1493070967418717996705171e-4, -0.1046450930688891587354327e-4, -0.7294971485088477169986746e-5, -0.5058237141326785665552064e-5, -0.3488590416297032549927031e-5, -0.2393206427093938070506012e-5, -0.1633028318374209170743394e-5, -0.1108394815502115127316820e-5, -0.7483179321690142728739359e-6, -0.5025418723896900527555212e-6, -0.3357037469306895805115546e-6, -0.2230700306981556484079346e-6, -0.1474451577404705893471723e-6, -0.9694537142843821183145493e-7, -0.6340650817983165854183039e-7, -0.4125281597997292543454039e-7, -0.2669863608647444234432417e-7, -0.1718869397329539903528673e-7, -0.1100823095953252158935162e-7, -0.7013187829205346730804204e-8, -0.4444665113656971914920979e-8, -0.2802144497835918309456751e-8, -0.1757406038399392007880848e-8, -0.1096442676719878283524089e-8, -0.6805092493832370091384262e-9, -0.4201635819811978308984480e-9, -0.2580720549398903308510481e-9, -0.1576898051707325645824557e-9, -0.9585353270320148521118371e-10, -0.5796372027032496381736661e-10, -0.3486981951439767325186431e-10, -0.2086844614201629359434107e-10, -0.1242450483517188985330601e-10, -0.7358989436838238028175315e-11, -0.4336195837012716989509190e-11, -0.2541866144559293225048769e-11, -0.1482350707216456169596291e-11, -0.8600132295160969048704279e-12, -0.4963825648030345884941720e-12, -0.2850272799994640993351100e-12, -0.1628231410435433343915847e-12, -0.9253517530796568988711767e-13, -0.5231904387078439423734991e-13, -0.2942904274907536637035087e-13, -0.1646861209472934265701707e-13, -0.9168609972068950589419375e-14, -0.5078280768842531755862938e-14, -0.2798321959684086361623925e-14, -0.1534077985990025530178263e-14, -0.8366946223931157801875458e-15, -0.4540014839572489640421670e-15, -0.2450864324006565520585709e-15, -0.1316297011679965318337360e-15, -0.7033347094398993022030766e-16, -0.3738906588834781501200156e-16, -0.1977436055729519304364136e-16, -0.1040486355537857239908506e-16, -0.5446873085247993592442947e-17, -0.2836846572016980047452363e-17, -0.1469951297806504842876013e-17, -0.7577907726628295065637298e-18, -0.3886652327556223671914838e-18, -0.1983274447591697794634031e-18, -0.1006865346010664339728430e-18, -0.5085599093462560019056651e-19, -0.2555616473221360979839205e-19, -0.1277711291477349028381922e-19, -0.6355561617974547678564100e-20, -0.3145284379748115775839534e-20, -0.1548642984144385532194339e-20, -0.7586277364385535380007560e-21, -0.3697368508385495481212434e-21, -0.1792850002167444277197814e-21, -0.8649339487208141711410640e-22, -0.4151549880751819128657313e-22, -0.1982560526365887292005855e-22, -0.9419591402219956768405243e-23, -0.4452742857507067242031201e-23, -0.2094178149147388017585982e-23, -0.9799199383965174477667876e-24, -0.4562039303075778937781093e-24, -0.2113096807073358619927786e-24, -0.9738054125666016460529380e-25, -0.4464962955517461045769742e-25, -0.2036839830996770073279630e-25, -0.9244633325579509781433326e-26, -0.4174617922924968276183391e-26, -0.1875592296561359766067593e-26, -0.8384076547424474404764890e-27, -0.3728786627489159285725893e-27, -0.1649968834419055881014869e-27, -0.7264074023243377877657008e-28, -0.3181863066343386789136187e-28, -0.1386691329625598948075213e-28, -0.6012783734099460236172624e-29, -0.2593995437123362612886143e-29, -0.1113425178718492778355866e-29, -0.4755009983792073461050496e-30, -0.2020415749389589696795519e-30, -0.8541405110545145479519840e-31, -0.3592671419230207088768861e-31, -0.1503507555679300913224246e-31, -0.6260283436716785719346509e-32, -0.2593480377514370417261009e-32, -0.1068988029132498238513063e-32, -0.4383933266292682172809914e-33, -0.1788778436796033153181937e-33, -0.7261912176216306101089190e-34, -0.2933239704874698217172402e-34, -0.1178817380216022663848294e-34, -0.4713550938665925243747415e-35, -0.1875222736937308593811831e-35, -0.7422680608185535408905020e-36, -0.2923292133270549875473422e-36, -0.1145479868926911875642964e-36, -0.4465877102072613609496200e-37, -0.1732329082290364039482100e-37, -0.6685880402092324407358875e-38, -0.2567388790315000103954881e-38, -0.9809113395522088573556313e-39, -0.3728835208268407801110216e-39, -0.1410334685901388337197457e-39, -0.5307340860010760817486761e-40, -0.1987182729569070557023125e-40, -0.7402951192281463566289795e-41, -0.2743964271316156357722060e-41 ], dtype=np.float64)
    h3 = np.array([ -0.7522527780636750492641059e0, -0.7447490315497708463240858e0, -0.7224619689626252165385118e0, -0.6860552061846493969863268e0, -0.6366054955061156295204758e0, -0.5755603365344096850483262e0, -0.5046815829547811446478382e0, -0.4259777864640005624125117e0, -0.3416285184773921405216660e0, -0.2539042236274465364534081e0, -0.1650852727968867264939651e0, -0.7738379667939842709258988e-1, 0.7128394424195324853014844e-2, 0.8658293927736663174097951e-1, 0.1593668102410841966827594e0, 0.2241613263920280449352809e0, 0.2799673824845877680517527e0, 0.3261167006652041288605015e0, 0.3622695948610319801705815e0, 0.3884003473857446343896496e0, 0.4047718038942624860766923e0, 0.4119011753186058824533937e0, 0.4105192820995319949018743e0, 0.4015255845130582620257648e0, 0.3859413195031716183649201e0, 0.3648629230000597762360636e0, 0.3394176769351978836202936e0, 0.3107232057693364099667621e0, 0.2798520840662402744643034e0, 0.2478024303401173430156194e0, 0.2154749773684402246897790e0, 0.1836567467116494732079552e0, 0.1530111326375332319918793e0, 0.1240739307148443832620940e0, 0.9725463688468146271051371e-1, 0.7284219701173870412977577e-1, 0.5101430368585303674221369e-1, 0.3184931174142700893159512e-1, 0.1533986919450959655382290e-1, 0.1407426811309193306581366e-2, -0.1008311291608286074413380e-1, -0.1930922840812282398312132e-1, -0.2647758532035030682089135e-1, -0.3181217775839225922486926e-1, -0.3554404023046894464526427e-1, -0.3790265208183702749516685e-1, -0.3910905737306063850349279e-1, -0.3937064210715186736633504e-1, -0.3887744829978686271653342e-1, -0.3779986028416367095012508e-1, -0.3628747152011772566083547e-1, -0.3446892799961155950489723e-1, -0.3245254463375208029954651e-1, -0.3032750110251363953076864e-1, -0.2816544089164076874994184e-1, -0.2602231914851994604543481e-1, -0.2394036936359898584929537e-1, -0.2195008388641825247433045e-1, -0.2007212746338689903391700e-1, -0.1831912527214265469865516e-1, -0.1669728661861120572688442e-1, -0.1520784216814043766189564e-1, -0.1384828617477219420839203e-1, -0.1261342573197174928239427e-1, -0.1149624682246302216128454e-1, -0.1048861222035593117850278e-1, -0.9581809474549548274726564e-2, -0.8766968673914992518412266e-2, -0.8035369845963356580758239e-2, -0.7378659024311709843220737e-2, -0.6788990545369120409265684e-2, -0.6259111260511144290061333e-2, -0.5782400284632080908741386e-2, -0.5352875804464578036313191e-2, -0.4965178455311671875710459e-2, -0.4614538919616485527188256e-2, -0.4296735750484013517713710e-2, -0.4008047998562558651176877e-2, -0.3745206023826233664801882e-2, -0.3505342894046476979204381e-2, -0.3285947990022833548498951e-2, -0.3084823830238963251792028e-2, -0.2900046668982056656687612e-2, -0.2729931086807768375811907e-2, -0.2572998556853316466871207e-2, -0.2427949813646523181953355e-2, -0.2293640754330915732383722e-2, -0.2169061550185197106672818e-2, -0.2053318626361484792588433e-2, -0.1945619169898585865047079e-2, -0.1845257842557062274985012e-2, -0.1751605400071271234291063e-2, -0.1664098948801722796139379e-2, -0.1582233601544145935191528e-2, -0.1505555324435757496173641e-2, -0.1433654795260900326865144e-2, -0.1366162119305863305428748e-2, -0.1302742271937752484738341e-2, -0.1243091157235637593921277e-2, -0.1186932189400779713774489e-2, -0.1134013318531012910469058e-2, -0.1084104434925714219487149e-2, -0.1036995096671516116549004e-2, -0.9924925341187004927105684e-3, -0.9504198922493585737226438e-3, -0.9106146780909950790852145e-3, -0.8729273854455090856168734e-3, -0.8372202734577421999252958e-3, -0.8033662790881490171689315e-3, -0.7712480465049772662387464e-3, -0.7407570588761368843162862e-3, -0.7117928601052224681383490e-3, -0.6842623557902678206459998e-3, -0.6580791841453911032352388e-3, -0.6331631488616646148452257e-3, -0.6094397069328185150662371e-3, -0.5868395053652243037188589e-3, -0.5652979614557357816469240e-3, -0.5447548819764808379193485e-3, -0.5251541171699206704315699e-3, -0.5064432459446979814905582e-3, -0.4885732890847829717111949e-3, -0.4714984476509869340551945e-3, -0.4551758640732029088500233e-3, -0.4395654037105695480727411e-3, -0.4246294549008608587718018e-3, -0.4103327457346023732872108e-3, -0.3966421759777806984761265e-3, -0.3835266627330082944382909e-3, -0.3709569985755748701109446e-3, -0.3589057210304776810509891e-3, -0.3473469923714317173865229e-3, -0.3362564888248703524021643e-3, -0.3256112983526542094353014e-3, -0.3153898262679901745636708e-3, -0.3055717080111181576022737e-3, -0.2961377284756872027881530e-3, -0.2870697473343167903391904e-3, -0.2783506298634098374691914e-3, -0.2699641828135376810549337e-3, -0.2618950949132550960609061e-3, -0.2541288816315519571599965e-3, -0.2466518338577700959600751e-3, -0.2394509701881161861915701e-3, -0.2325139925352426415436720e-3, -0.2258292448020649292499711e-3, -0.2193856743833149971866920e-3, -0.2131727962785441468085678e-3, -0.2071806596186039850962257e-3, -0.2013998164242456949121338e-3, -0.1958212924305587453675523e-3, -0.1904365598246742268269672e-3, -0.1852375117566223449189077e-3, -0.1802164384945805472907308e-3, -0.1753660051060874920343825e-3, -0.1706792305562262391906103e-3, -0.1661494681223850440721571e-3, -0.1617703870330642541013594e-3, -0.1575359552453832883093564e-3, -0.1534404232825155716084045e-3, -0.1494783090582982775062280e-3, -0.1456443836217787948749789e-3, -0.1419336577595168918308957e-3, -0.1383413693981019940302776e-3, -0.1348629717536061671270311e-3, -0.1314941221786090162018978e-3, -0.1282306716610312631043834e-3, -0.1250686549323268134999138e-3, -0.1220042811456336331711188e-3, -0.1190339250872943430156140e-3, -0.1161541188877486230913414e-3, -0.1133615442001899065679247e-3, -0.1106530248175853517419676e-3, -0.1080255197006960803598953e-3, -0.1054761163916181391183883e-3, -0.1030020247891063146774180e-3, -0.1006005712635544029343839e-3, -0.9826919309099737327798045e-4, -0.9600543318688272806740460e-4, -0.9380693512163903486436983e-4, -0.9167143840125715403094134e-4, -0.8959677399720145006388879e-4, -0.8758086011099098595144745e-4, -0.8562169815974051700802759e-4, -0.8371736896983366064768422e-4, -0.8186602916672109476829247e-4, -0.8006590774959976520266573e-4, -0.7831530284043921555152064e-4, -0.7661257859748228262605498e-4, -0.7495616228396319961002592e-4, -0.7334454148335998246272097e-4, -0.7177626145303295708079228e-4, -0.7024992260860025649833230e-4, -0.6876417813186671874001603e-4, -0.6731773169555726054493046e-4, -0.6590933529851172806481185e-4, -0.6453778720537748581672358e-4, -0.6320192998519050404738797e-4, -0.6190064864356719221383246e-4, -0.6063286884353932444622322e-4, -0.5939755521035460581086281e-4, -0.5819370971583712468698264e-4 ], dtype=np.float64)

    v=vin
    # Voigt function is symmetric, so -v = v
    if len(np.argwhere(v<0.0)) != 0: v[np.argwhere(v<0.0)] *= -1.0
    # if a is exactly zero go to 3 for exact expression
    if (a == 0.0):
        voigt_prof = np.exp(-(v*v))
        return voigt_prof
    # Scale up v for ease with lookup tables
    v0 = v*10.0
    n=np.array(v0,dtype=np.int_)
    voigt_prof = np.zeros(np.size(vin))
    nl=np.argwhere(n<100)
    nh=np.argwhere(n>=100)
    if len(nh) != 0:
        r=1.0/v[nh]**2
        voigt_prof[nh] = a*r*oneonsqrtpi*(1.0 + r*(1.5 + r*(3.75 + r*(13.125 + 59.0625*r))) - a*a*r*(1.0 + r*(5.0 +26.25*r)))
    if len(nl) != 0:
        v0[nl] = 2*v[nl]*10.0
        p=np.int_(v0[nl])
        p1=p+1
        p2=p+2
        x=0.5*np.int_(v0[nl])
        y=x+0.5
        z=x+1.0
        v1 = v0[nl] * 0.5
        voigt_prof[nl] = 2.0*((v1-y)*(v1-z)*(h0[p]+a*(h1[p]+a*(h2[p]+a*h3[p]))) - (v1-x)*(v1-z)*2.0*(h0[p1] + a*(h1[p1]+a*(h2[p1]+a*h3[p1]))) + (v1-x)*(v1-y)*(h0[p2] + a*(h1[p2]+a*(h2[p2]+a*h3[p2]))))
    del nl, nh
    return voigt_prof


# The primary call
def voigt_model(iwave, line, fwhm=None, flg_ret=1, debug=False, 
    skip_wveval=False):
    '''Generates a Voigt model from a line or list of lines
    This will run *slowly* for many many lines

    Parameters:
    ------------
    wave: Quantity array
      Observed wavelengths
    line: AbsLine, List of Absline, or array of parameters
    skip_wveval: bool, optional [False]
      Skip wavelength check
      If False, the median dwave value is calculated and compared against
      1/10 of the b-value of the input line(s).  
      If necessary, the wavelenght array is rebinned for the calculation
      and the final array is rebinned to the original.
    fwhm: float, optional [None]
      FWHM for Gaussian smoothing (pixels)
    flg_ret : int (1)  Byte-wise Flag for return
      1: vmodel [XSpectrum1D]
      2: tau
      4: Absorbed flux [np.ndarray]
    ToDo:
        1.  May need to more finely sample the wavelength array
    '''
    # Wavelength input
    if not isinstance(iwave,Quantity):  # Standard wavelength array
        raise ValueError('voigt_model: Unknown spectrum input')

    # Demand that the evaluation delta wavelength is < 1/10 of the b-value
    flg_rebin = 0
    if not skip_wveval:
        if isinstance(line,AbsLine):  # Single line as a AbsLine Class
            minb = line.attrib['b']
        else:
            minb = np.min(np.array(
                [iline.attrib['b'].value for iline in line]))*u.km/u.s
        # Calculate dwave
        dwave = np.median(np.abs(iwave-np.roll(iwave,1)))
        medwave = np.median(iwave)
        warnings.warn('Using a sub-grid wavelength array because the input array is too coarse.')
        if const.c.to('km/s')*dwave/medwave > minb/10.:
            wmin = np.min(iwave.to('AA').value)
            wmax = np.max(iwave.to('AA').value)
            nsub = int(np.round( (np.log10(wmax)- np.log10(wmin)) / 1.449E-6)) + 1
            wave = 10.**(np.log10(wmin) + np.arange(nsub)*1.449E-6) * u.AA
            flg_rebin = 1
        else:
            wave = iwave
    else: # No evaluation 
        wave = iwave

    # Line input
    if isinstance(line,AbsLine):  # Single line as a AbsLine Class
        pass
        #par = [0*i for i in range(6)] # Dummy list
        #par[0] = line.attrib['N'] # logN; Won't have units
        #par[1] = line.attrib['z']
        #par[2] = line.attrib['b'] # Should have units
        #par[3] = line.wrest # Should have units
        #par[4] = line.data['f']
        #par[5] = line.data['gamma'] # Should have units
    elif isinstance(line,list):
        if isinstance(line[0],AbsLine):  # List of Abs_Line
            tau = np.zeros(len(wave))
            for iline in line:
                if debug:
                    print(iline)
                tau += voigt_model(wave, iline, fwhm=0., 
                    flg_ret=2, debug=debug, skip_wveval=True) 
        else:
            raise ValueError('voigt: Unknown type for voigt line in your list')
    else: 
        raise ValueError('voigt: Unknown type for voigt line')

    # tau
    if 'tau' not in locals():
        #cold = 10.0**par[0] / u.cm / u.cm
        cold = 10.0**line.attrib['N'] / u.cm / u.cm
        #zp1=par[1]+1.0
        zp1=line.attrib['z']+1.0

        #wv=par[3].to(u.cm) #*1.0e-8
        wv=line.wrest.to(u.cm) #*1.0e-8
        nujk = (const.c / wv).to(u.Hz)
        #dnu = (par[2].to(u.km/u.s) / wv).to('Hz')
        dnu = (line.attrib['b'].to(u.km/u.s) / wv).to('Hz')
        if line.data['gamma'].value == 0.:
            warnings.warn('Gamma value is probably not set for wrest={:g} {}!'
                .format(float(line.wrest.value),line.wrest.unit))
        avoigt = (line.data['gamma']/( 4 * np.pi * dnu)).to(u.dimensionless_unscaled)

        uvoigt = ( ((const.c / (wave/zp1)) - nujk) / dnu).to(u.dimensionless_unscaled)

        # Voigt
        cne = 0.014971475 * cold * line.data['f'] * u.cm * u.cm * u.Hz
        try:
            tau = cne * voigtking(uvoigt,avoigt) / dnu #(np.sqrt(np.pi) * dnu)
        except IndexError:
            pass
        tau = tau.value # Should be dimensionless

    # Only tau?
    if flg_ret == 2:
        return tau
    # Flux
    flux = np.exp(-1.0*tau)
    vmodel = XSpectrum1D.from_tuple((wave,flux))

    # Rebin?
    if flg_rebin:
        vmodel = vmodel.rebin(iwave)
    # Convolve
    if fwhm is not None:
        vmodel.gauss_smooth(fwhm=fwhm)
    else:
        warnings.warn('Assuming infinite spectral resolution, i.e. no smoothing.')
        warnings.warn('Set fwhm to smooth.')
    
    # Return
    ret_val = []
    if flg_ret % 2 == 1: ret_val.append(vmodel)
    if flg_ret % 4 >= 2: ret_val.append(tau)
    if flg_ret % 8 >= 4: ret_val.append(vmodel.flux.value)
    if len(ret_val) == 1: ret_val = ret_val[0]
    return ret_val

