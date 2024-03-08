<?php

namespace App\Controllers;

class EchoController extends BaseController
{
    public function index()
    {
        $id = $this->request->getVar('id');
        $taint = $this->request->getVar('taint');


        $data = [
            'form' => [
                'id' => $id,
                'taint' => $taint
            ]
        ];

        return $this->response->setJSON($data);
    }
}
