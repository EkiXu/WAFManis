package models

func init() {

}

type Message struct {
	Id    string `json:"id" form:"id"`
	Taint string `json:"taint" form:"taint"`
}
