"""
Testes unitários para validar as operações matemáticas e os conversores.
"""

import unittest
from fractions import Fraction
import math_operations as mo
import converters as cv


class TestMathOperations(unittest.TestCase):
    def test_operacoes_basicas(self):
        self.assertEqual(mo.somar(10, 5), 15)
        self.assertEqual(mo.subtrair(10, 5), 5)
        self.assertEqual(mo.multiplicar(10, 5), 50)
        self.assertEqual(mo.dividir(10, 5), 2.0)
        self.assertIn("Erro", mo.dividir(10, 0))

    def test_porcentagem(self):
        # 15% de 200 = 30
        self.assertEqual(mo.calcular_porcentagem(200, 15, "taxa"), 30.0)
        # 50 de 200 = 25%
        self.assertEqual(mo.calcular_porcentagem(50, 200, "valor_sobre_total"), 25.0)
        # 100 + 10% = 110
        self.assertEqual(mo.calcular_porcentagem(100, 10, "adicionar_taxa"), 110.0)
        # 100 - 10% = 90
        self.assertEqual(mo.calcular_porcentagem(100, 10, "descontar_taxa"), 90.0)

    def test_exponenciacao(self):
        self.assertEqual(mo.exponenciacao(2, 3), 8.0)
        self.assertEqual(mo.exponenciacao(5, 0), 1.0)
        self.assertEqual(mo.exponenciacao(4, 0.5), 2.0)
        self.assertIn("Erro", mo.exponenciacao(0, -2))

    def test_radiciacao(self):
        self.assertEqual(mo.radiciacao(16, 2), 4.0)
        self.assertAlmostEqual(mo.radiciacao(27, 3), 3.0)
        self.assertIn("Erro", mo.radiciacao(-4, 2))
        # Raiz cúbica de número negativo é válida
        self.assertAlmostEqual(mo.radiciacao(-8, 3), -2.0)
        self.assertIn("Erro", mo.radiciacao(16, 0))

    def test_fracao(self):
        # 1/2 + 1/4 = 3/4
        res = mo.calcular_fracao(1, 2, "+", 1, 4)
        self.assertIsInstance(res, tuple)
        self.assertEqual(res[0], Fraction(3, 4))
        self.assertEqual(res[2], 0.75)

        # 3/2 * 4/3 = 2
        res2 = mo.calcular_fracao(3, 2, "*", 4, 3)
        self.assertEqual(res2[0], Fraction(2, 1))

        # Divisão por zero no denominador
        self.assertIn("Erro", mo.calcular_fracao(1, 0, "+", 1, 2))

    def test_avaliar_expressao_segura(self):
        self.assertEqual(mo.avaliar_expressao_segura("2 + 3 * 4"), 14.0)
        self.assertEqual(mo.avaliar_expressao_segura("(2 + 3) * 4"), 20.0)
        self.assertEqual(mo.avaliar_expressao_segura("2 ^ 3"), 8.0)
        self.assertEqual(mo.avaliar_expressao_segura("10 ÷ 2"), 5.0)
        self.assertEqual(mo.avaliar_expressao_segura("15 × 3"), 45.0)
        self.assertIn("Erro", mo.avaliar_expressao_segura("10 / 0"))



class TestConverters(unittest.TestCase):
    def test_conversor_comprimento(self):
        # 1 km = 1000 m
        self.assertEqual(cv.converter_comprimento(1, "km", "m"), 1000.0)
        # 1 m = 100 cm
        self.assertEqual(cv.converter_comprimento(1, "m", "cm"), 100.0)
        # 1 polegada = 2.54 cm
        self.assertAlmostEqual(cv.converter_comprimento(1, "polegadas", "cm"), 2.54)
        # 1 milha em km
        self.assertAlmostEqual(cv.converter_comprimento(1, "milhas", "km"), 1.609344)
        # 1 jarda = 3 pés
        self.assertAlmostEqual(cv.converter_comprimento(1, "jardas", "pés"), 3.0)

    def test_conversor_volume(self):
        # 1 m³ = 1000 L
        self.assertEqual(cv.converter_volume(1, "m³", "L"), 1000.0)
        # 1 L = 1000 cm³
        self.assertEqual(cv.converter_volume(1, "L", "cm³"), 1000.0)
        # 1 m³ = 1.000.000 cm³
        self.assertEqual(cv.converter_volume(1, "m³", "cm³"), 1_000_000.0)


if __name__ == "__main__":
    unittest.main()
