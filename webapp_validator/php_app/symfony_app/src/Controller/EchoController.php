<?php

namespace App\Controller;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class EchoController extends AbstractController
{
    /**
    * @Route("/", name="post")
    */
    public function post(Request $request)
    {
        $id = $request->get("id");
        $taint = $request->get("taint");

        $data = [
            'form' => [
                'id' => $id,
                'taint' => $taint
            ]
        ];

        return new Response(json_encode($data), Response::HTTP_OK,
            ['content-type' => 'application/json']);
    }
}
