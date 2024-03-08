package controllers

import (
	"beeapp/models"
	"fmt"

	beego "github.com/beego/beego/v2/server/web"
)

// Operations about Users
type EchoController struct {
	beego.Controller
}

// @Title CreateUser
// @Description create users
// @Param	body		body 	models.User	true		"body for user content"
// @Success 200 {int} models.User.Id
// @Failure 403 body is empty
// @router / [post]
func (u *EchoController) Post() {
	var message models.Message
	if err := u.ParseForm(&message); err != nil {
		//handle error
		fmt.Errorf("+%v", err)
	}
	u.Data["json"] = map[string]map[string]string{"form": {"id": message.Id, "taint": message.Taint}}
	u.ServeJSON()
}
