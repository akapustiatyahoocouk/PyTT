"""
    GUI skin API.
"""
from typing import TypeAlias

import skin_impl.ISkin
import skin_impl.SkinRegistry
import skin_impl.ActiveSkin

ISkin: TypeAlias = skin_impl.ISkin.ISkin
SkinRegistry: TypeAlias = skin_impl.SkinRegistry.SkinRegistry
ActiveSkin: TypeAlias = skin_impl.ActiveSkin.ActiveSkin

import admin_skin_impl.AdminSkin
#skin_impl.SkinRegistry.SkinRegistry.register_skin(admin_skin_impl.AdminSkin.AdminSkin.instance)
