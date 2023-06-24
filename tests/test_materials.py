import unittest
from timberas.material import TimberMaterial
#from timberas.utils import ApplicationCategory

class TestTimberMaterial(unittest.TestCase):
    def setUp(self):
        self.timber_material = TimberMaterial(name='test', grade='grade1', 
                                              seasoned=True, grade_type='F', 
                                              f_b=1.0, f_t=2.0, f_s=3.0, 
                                              f_c=4.0, E=5, G=6, 
                                              density=7.0, phi_1=0.1, 
                                              phi_2=0.2, phi_3=0.3)
        self.timber_material_GL = TimberMaterial(name='testGL', grade='grade2', 
                                              seasoned=True, grade_type='GL', 
                                              f_b=1.0, f_t=2.0, f_s=3.0, 
                                              f_c=4.0, E=5, G=6, 
                                              density=7.0, phi_1=0.1, 
                                              phi_2=0.2, phi_3=0.3)        

    def test_phi(self):
        self.assertEqual(self.timber_material.phi(1), 0.1)
        self.assertEqual(self.timber_material.phi(2), 0.2)
        self.assertEqual(self.timber_material.phi(3), 0.3)
        with self.assertRaises(ValueError):
            self.timber_material.phi('UnknownCategory')

    def test_update_f_t(self):
        self.timber_material.update_f_t(200)
        self.assertAlmostEqual(self.timber_material.f_t, 2, places=3)
        self.timber_material_GL.update_f_t(150)
        self.assertAlmostEqual(self.timber_material_GL.f_t, 2, places=3)
        self.timber_material_GL.update_f_t(200)
        self.assertAlmostEqual(self.timber_material_GL.f_t, 1.906, places=3)
        
    def test_from_dict(self):
        dict_material = {'name': 'test2', 'grade': 'grade2', 
                         'seasoned': False, 'grade_type': 'M', 
                         'f_b': 10.0, 'f_t': 20.0, 'f_s': 30.0, 
                         'f_c': 40.0, 'E': 50, 'G': 60, 
                         'density': 70.0, 'phi_1': 0.4, 
                         'phi_2': 0.5, 'phi_3': 0.6}
        timber_material = TimberMaterial.from_dict(**dict_material)
        self.assertEqual(timber_material.name, 'test2')
        self.assertEqual(timber_material.grade, 'grade2')
        self.assertFalse(timber_material.seasoned)
        self.assertEqual(timber_material.grade_type, 'M')
        self.assertEqual(timber_material.f_b, 10.0)
        self.assertEqual(timber_material.f_t, 20.0)
        self.assertEqual(timber_material.f_s, 30.0)
        self.assertEqual(timber_material.f_c, 40.0)
        self.assertEqual(timber_material.E, 50)
        self.assertEqual(timber_material.G, 60)
        self.assertEqual(timber_material.density, 70.0)
        self.assertEqual(timber_material.phi_1, 0.4)
        self.assertEqual(timber_material.phi_2, 0.5)
        self.assertEqual(timber_material.phi_3, 0.6)

    def test_from_library(self):
        material_from_library = TimberMaterial.from_library('MGP10')
        self.assertEqual(material_from_library.name, 'MGP10')
        self.assertEqual(material_from_library.grade, 'MGP10')
        self.assertTrue(material_from_library.seasoned)
        self.assertEqual(material_from_library.grade_type, 'MGP')
        self.assertEqual(material_from_library.f_b, 17.0)
        self.assertEqual(material_from_library.f_t, 7.7)
        self.assertEqual(material_from_library.f_s, 2.6)
        self.assertEqual(material_from_library.f_c, 18)
        self.assertEqual(material_from_library.E, 10000)
        #self.assertEqual(material_from_library.G, )
        self.assertEqual(material_from_library.density, 670)
        self.assertEqual(material_from_library.phi_1, 0.95)
        self.assertEqual(material_from_library.phi_2, 0.85)
        self.assertEqual(material_from_library.phi_3, 0.75)

if __name__ == '__main__':
    unittest.main()
