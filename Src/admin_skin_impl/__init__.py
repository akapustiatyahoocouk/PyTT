from typing import final

print('Loading package', __file__)

from annotations import classproperty
import pnp_impl.Plugin
import skin_impl.ISkin

@final
class AdminSkinPlugin(pnp_impl.Plugin.Plugin):
    
    ##########
    #   Singleton
    __instance : "AdminSkinPlugin" = None

    def __init__(self):
        assert AdminSkinPlugin.__instance is None, "Use AdminSkinPlugin.instance instead"
        super().__init__()
    
    @classproperty
    def instance(cls) -> "AdminSkinPlugin":
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
        pass

AdminSkinPlugin.instance
# TODO kill off admin_skin_plugin = AdminSkinPlugin.instance
