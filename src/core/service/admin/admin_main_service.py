from aiogram import Router, types


admin_router: Router = Router(name="admin")


@admin_router.message(message: types.CallbackQuery(""))
async def meets()