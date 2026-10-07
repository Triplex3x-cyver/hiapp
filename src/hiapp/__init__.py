"""
Hiapp: H.ogar con I.nteligencia A.rtificial P.rivada P.ersonal.

Asistente de voz autogestionado para el hogar, con servidor de juegos
para PPSSPP y otras aplicaciones.
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("hiapp")
except PackageNotFoundError:
    # Para estado en desarrollo, sin pip install
    __version__ = "0.0.0+unknown"

__author__ = "Dixan Pupo Morales (Triplex3x-cyver)"
__license__ = "Apache-2.0"
