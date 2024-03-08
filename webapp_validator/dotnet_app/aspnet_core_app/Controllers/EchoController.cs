using Microsoft.AspNetCore.Mvc;

namespace fuzz_aspnet_core.Controllers;

[ApiController]
[Route("[controller]")]
public class EchoController : Controller
{
    [HttpPost]
    [Route("post")]
    public async Task<IActionResult> Echo([FromForm]EchoDto echoDto)
    {
        return Json(new
        {
            form = new {
                taint = echoDto.taint,
                id = echoDto.id
            },
        });
    }
}

public class EchoDto
{
    public string? taint { get; set; }
    public string? id { get; set; }
    public IFormFile? Photo { get; set; }
}
