
# -*- coding: utf-8 -*-

# Test LCC functions and methods.

__all__ = ('Tests',)
__version__ = '17.06.16'

from base import TestsBase

from pygeodesy import F_D, F_DMS, Conic, Conics, Datums, Lcc, toLcc


class Tests(TestsBase):

    def testConic(self, module, n=''):

        self.subtitle(module, 'Conic')

        LatLon = module.LatLon

        n = 'Snyder' + str(n)
        # Snyder, pp 297 <http://pubs.er.USGS.gov/djvu/PP/PP_1395.pdf>
        c = Conic(LatLon(23, -96, datum=Datums.NAD27), 33, 45, E0=0, N0=0, name=n)
        self.test(n, c, "name='%s', lat0=23.0, lon0=-96.0, par1=33.0, par2=45.0, E0=0, N0=0, k0=1, SP=2, datum=(name='NAD27', ellipsoid=Ellipsoids.Clarke1866, transform=Transforms.NAD27)" % (n,))

    def testLcc(self, module):

        self.subtitle(module, 'Lcc')

        LatLon = module.LatLon

        lb = Lcc(448251, 5411932.0001)
        self.test('lb1', lb.toStr(4), '448251.0 5411932.0001')
        self.test('lb1', lb.toStr(sep=', '), '448251, 5411932')
        self.test('lb1', lb.conic.name2, 'WRF_Lb.WGS84')

        ll = LatLon(46.5, 3)
        self.test('LatLon', ll, '46.5°N, 003.0°E')
        self.test('LatLon', ll.toStr(form=F_DMS), '46°30′00.0″N, 003°00′00.0″E')
        lb = toLcc(ll, conic=Conics.Fr93Lb)
        self.test('toLcc1', str(lb), '700000 6600000')
        self.test('toLcc1', lb.toLatLon(LatLon), '46.5°N, 003.0°E')

        lb = Lcc(1894410.9, 1564649.5, conic=Conics.Snyder)
        self.test('lb2', lb, '1894411 1564650')
        self.test('lb2', lb.conic.datum.ellipsoid.name, 'Clarke1866')
        ll = lb.toLatLon(LatLon)  # Clark1866
        self.test('toLatLon2', ll.toStr(prec=6, form=F_D), '35.0°N, 075.0°W')
        self.test('toLatLon2', ll.toStr(prec=4, form=F_DMS), '35°00′00.0007″N, 074°59′59.9997″W')
        self.test('toLatLon2', ll.datum.name, 'NAD27')
        lb = toLcc(ll, conic=Conics.Snyder)
        self.test('toLcc2', lb.toStr(prec=1), '1894410.9 1564649.5')
        self.test('toLcc2', lb.conic.name2, 'Snyder.NAD27')

        for n, c in sorted(Conics.items()):
            d = abs(c.par1 - c.par2)
            if d > 0:  # test corners of the conic
                for ll in (LatLon(c.par1, c.lon0 - d, datum=c.datum),
                           LatLon(c.par1, c.lon0,     datum=c.datum),
                           LatLon(c.par1, c.lon0 + d, datum=c.datum),
                           LatLon(c.par2, c.lon0 - d, datum=c.datum),
                           LatLon(c.par2, c.lon0,     datum=c.datum),
                           LatLon(c.par2, c.lon0 + d, datum=c.datum)):
#                   self.test(n, ll, str(ll))  # PYCHOK expected
                    lb = toLcc(ll, conic=c)
#                   self.test(n, lb, '')
                    ll_ = lb.toLatLon(LatLon)
                    self.test(n, ll, str(ll_))
                    self.test(n, ll.datum.name, ll_.datum.name)


if __name__ == '__main__':

    from pygeodesy import ellipsoidalNvector, ellipsoidalVincenty, lcc

    # Snyder, pp 297 <http://pubs.er.USGS.gov/djvu/PP/PP_1395.pdf>
    Conic(ellipsoidalVincenty.LatLon(23, -96, datum=Datums.NAD27),
                                     33, 45, E0=0, N0=0, name='Snyder')

    t = Tests(__file__, __version__, lcc)

    t.testLcc(ellipsoidalNvector)
    t.testLcc(ellipsoidalVincenty)

    t.testConic(ellipsoidalNvector, 'N')
    t.testConic(ellipsoidalVincenty, 'V')

    for n in ('', 'N', 'V'):
        Conics.unregister('Snyder' + n)

    t.results()
    t.exit()
