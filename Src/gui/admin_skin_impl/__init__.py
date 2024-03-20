import gui.skin as skinapi
import gui.admin_skin_impl.AdminSkin as adminskin

print('initialising gui.admin_skin_impl package')

skinapi.SkinRegistry.register_skin(adminskin.AdminSkin.instance())


