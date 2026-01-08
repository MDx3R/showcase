"""Certificate type value object."""

from enum import Enum


class CertificateType(str, Enum):
    """Type of certificate."""

    CERTIFICATE = "certificate"
    DIPLOMA = "diploma"
    ATTESTATION = "attestation"
    NONE = "none"
