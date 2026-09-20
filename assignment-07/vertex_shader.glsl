#version 330 core
layout (location = 0) in vec4 vertexPosition;
layout (location = 1) in vec4 vertexColor;
layout (location = 2) in vec2 vertexUV;
layout (location = 3) in vec4 vertexNormal;


out vec4 fragColor;
out vec2 fragUV;
out vec3 fragNormal;
out vec3 fragPos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

void main()
{
    gl_Position = proj * view * model * vertexPosition;

    fragPos = vec3(model * vertexPosition);
    fragNormal = normalize(mat3(transpose(inverse(model))) * vec3(vertexNormal));

    fragColor = vertexColor;
    fragUV = vertexUV;
}