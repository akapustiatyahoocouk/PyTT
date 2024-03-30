"""
    Package declarations for admin_skin_impl package.
"""
print('Loading package', __file__)

from typing import final

from util.Annotations import staticproperty
from pnp.Plugin import Plugin
from gui.skins.Skin import Skin

@final
class AdminSkinPlugin(Plugin):
    
    ##########
    #   Singleton
    __instance : "AdminSkinPlugin" = None

    def __init__(self):
        assert AdminSkinPlugin.__instance is None, "Use AdminSkinPlugin.instance instead"
        super().__init__()
    
    @staticproperty
    def instance() -> "AdminSkinPlugin":
        """
            Returns one and only instance of this class, creating
            it on the first call.
            
            @return:
                The one and only instance of this class.
        """
        if AdminSkinPlugin.__instance is None:
            AdminSkinPlugin.__instance = AdminSkinPlugin()
        return AdminSkinPlugin.__instance

    ##########
    #   Plugin
    @property
    def display_name(self) -> str:
        return "Admin skin"

    def initialize(self) -> None:
        from gui.skins.SkinRegistry import SkinRegistry
        from gui.skins.admin.AdminSkin import AdminSkin
        SkinRegistry.register_skin(AdminSkin.instance)

AdminSkinPlugin.instance
