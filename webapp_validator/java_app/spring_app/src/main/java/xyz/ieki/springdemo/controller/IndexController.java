package xyz.ieki.springdemo.controller;

import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;

import javax.servlet.http.HttpServletRequest;
import java.io.BufferedOutputStream;
import java.io.FileOutputStream;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
public class IndexController {

    @RequestMapping(value = "/post", method = RequestMethod.POST, produces = "application/json")
    @PostMapping(consumes = MediaType.APPLICATION_FORM_URLENCODED_VALUE)
    public Map<String, Object> echo(@RequestParam Map<String, String> formData) {
        Map<String, Object> response = new HashMap<>();
        response.put("form", formData);
        return response;
    }

    @RequestMapping(value = "/post2", method = RequestMethod.POST, produces = "application/json")
    public  Map<String, Object> handleFileUpload(HttpServletRequest request) {
        MultipartHttpServletRequest params=((MultipartHttpServletRequest) request);
        List<MultipartFile> files = ((MultipartHttpServletRequest) request)
                .getFiles("file");
        String name=params.getParameter("name");
        Map<String, Object> response = new HashMap<>();
        response.put("form", params.getParameterMap());
        return response;
    }
}
