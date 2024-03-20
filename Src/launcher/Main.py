import gui.skin as skinapi

if __name__ == '__main__':
    #   Select the initial skin TODO properly!
    skinapi.ActiveSkin.set(skinapi.SkinRegistry.get_default_skin())

    #   Go!
    while True:
        skin_before : skinapi.ISkin = skinapi.ActiveSkin.get()
        if skin_before is None:
            break;
        skinapi.ActiveSkin.get().run_event_loop()
        skin_after : skinapi.ISkin = skinapi.ActiveSkin.get()
        if skin_after is None:
            break;
        if not (skin_after.is_active):
            break;
    
    #   Cleanup & exit
    skinapi.ActiveSkin.set(None)
    print('exit main loop')
