<?php

namespace App\Http\Controllers;
use Illuminate\Http\Request;

class EchoController extends Controller
{
    public function post(Request $request)
    {
        return response()->json([
            'form' => $request->all()
        ]);
    }
}
