Railroad crossing cleanup script
================================

I wanted a MapRoulette challenge exposing railroad level crossings in the US that may not exist as such in OSM.

I started with the DBF file that can be downloaded [from the FRA web site](http://safetydata.fra.dot.gov/OfficeofSafety/publicsite/downloaddbf.aspx).

![site](https://www.dropbox.com/s/eqbnfpy0x4epmeu/Screenshot%202015-07-01%2014.36.18.png?dl=1)

Converting this to CSV is not too bad:

`ogr2ogr -f CSV ~/tmp/crossings ~/Downloads/gcispubl.DBF`

But the CSV file is messy:

```
martijnv-mba:crossings martijnv$ head -n2 gcispubl.csv
CROSSING,EFFDATE,EDATE,REASON,STATE,CNTYCD,STATE2,CITYCD,NEAREST,RAILROAD,RRDIV,RRSUBDIV,HIGHWAY,STREET,RRID,TTSTN,BRANCH,MILEPOST,MAPREF,TYPEXING,POSXING,PRVCAT,PRVIND,PRVSIGN,INIT,BATCH,USERCD,UPDATE_,LINK,DAYTHRU,DAYSWT,NGHTTHRU,NGHTSWT,LT1MOV,MAXTTSPD,MINSPD,MAXSPD,MAINTRK,OTHRTRK,OTHRDES,SEPIND,SEPRR,SAMEIND,SAMERR,WDCODE,XBUCKRF,XBUCKNRF,STOPSTD,STOPOTH,OTHSGN1,OTHDES1,OTHSGN2,OTHDES2,GATERW,GATEOTH,FLASHOV,FLASHNOV,FLASHMAS,FLASHOTH,FLASHDES,HWYSGNL,WIGWAGS,BELLS,SPECPRO,NOSIGNS,COMPOWER,SGNLEQP,SPSEL,DEVELTYP,HWYPVED,DOWNST,PAVEMRK,HWYNEAR,ADVWARN,XANGLE,XSURFACE,TRAFICLN,TRUCKLN,STHWY1,HWYSYS,HWYCLASS,AADT,PCTTRUK,LATITUDE,LONGITUD,LLSOURCE,INTRPRMP,HUMPSIGN,HSCORRID,DOTACPD,ACPDDATE,ACCCNT1,ACCCNT2,ACCCNT3,ACCCNT4,ACCCNT5,HISTDATE,SCHLBUS,WHISTBAN,PASSCD,PASSCNT,RRMAIN,XINGOWNR,SOURCE,UPDATDAT,LONGBDAT,LONGEDAT,FOURQUAD,TWOQUAD,OPENPUB,RRNARR1,RRNARR2,RRNARR3,RRNARR4,STNARR1,STNARR2,STNARR3,STNARR4,AADTYEAR,AADTCALC,TRAINDAT,TRAINCAL,RESERVE1,RESERVE2,RESERVE3,RESERVE4,RESERVE5,DOTCASPD,DOTFATPD,FUNCCAT,RRCONT,HWYCONT,POLCONT,NARR,TOTALTRN,TOTALSWT,ENSSIGN,XBUCK,GATES,PRVSIGNL,FLASHPAI,WARNACTO,CHANNEL,XINGADJ,XNGADJNO,ILLUMINA,HWYSPEED,CNTYNAM,TTSTNNAM,CITYNAM,XSUROTHR,HWYNRSIG
009972A,140108,999999,1,20,C009,20,2150,1,KO,EASTERN,HUTCHINSON,T-222,AIRPORT ROAD,,586993,,027458,530,3,1,,,,2,140420,,C4,,1,1,1,1,0,25,10,20,1,0,,2,,2,,4,2,0,1,0,1,ADV WARN,0,,0,0,0,0,0,0,,0,0,0,,0,1,2,5,1,2,2,3,1,2,3,1,2,2,2,08,09,000057,08,383284258,-988478368,1,,,,0.003390,2013/05/31,0,0,0,0,0,2013/11/14,0,0,,0,,,P,2014/03/28,2014/01/08,,,,,,,,,,,,,2008,,,,,,,,,0.001271,0.000181,,,7852967121,8663869321,,4,2,,2,0,,0,,,,,,55,BARTON,DUNDEE,GREAT BEND,,
```

So I wrote this script to clean it up:

* Keep only the fields I want
* Properly format the coordinates

```
martijnv-mba:railways-csv-clean martijnv$ ./clean.py
reading...............
writing
out of 217027 rows in the input file, 111 rows failed.
done
```

Much cleaner:

```
EFFDATE,REASON,STREET,lon,lat
140108,1,AIRPORT ROAD,-98.8478368,38.3284258
```

(`REASON` is salient because value 3 means closed or abanoned. See  [this PDF](https://www.fra.dot.gov/elib/document/3088) for a field reference.

This can be converted into a Shapefile easily using the supplied VRT file:

```
ogr2ogr -f 'ESRI Shapefile' ~/tmp/crossings/shape ~/tmp/crossings/gcispubl.vrt
```

Yay results:

![results](https://www.dropbox.com/s/cng9lngvic0mxb0/Screenshot%202015-07-01%2015.00.27.png?dl=1)