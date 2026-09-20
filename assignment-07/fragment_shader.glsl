#version 330 core
out vec4 FragColor;

// Data from vertex shader
in vec4 fragColor;
in vec2 fragUV;
in vec3 fragNormal;
in vec3 fragPos;

// Material properties
uniform sampler2D tex1;
uniform sampler2D tex2;
uniform float blendFactor;
uniform float materialShininess;
uniform float materialSpecularStrength;

struct Light {
    int type; // 0:off, 1:directional, 2:point, 3:spot

    vec3 position;
    vec3 direction;

    vec3 color;
    float intensity;

    float constant;
    float linear;
    float quadratic;

    float coneAngle;
    float penumbraAngle;
};

#define MAX_LIGHTS 3
uniform Light lights[MAX_LIGHTS];
uniform vec3 viewPos;
uniform bool specularOn;

void main()
{
    vec4 texColor1 = texture(tex1, fragUV);
    vec4 texColor2 = texture(tex2, fragUV);
    vec4 blendedTexture = mix(texColor1, texColor2, blendFactor);

    vec3 norm = normalize(fragNormal);
    vec3 viewDir = normalize(viewPos - fragPos);
    vec3 finalColor = vec3(0.0);
    vec3 ambient = vec3(0.1);

    for(int i = 0; i < MAX_LIGHTS; i++)
    {
        if(lights[i].type == 0) continue;

        vec3 lightDir;
        float attenuation = 1.0;
        float spotlightEffect = 1.0;

        if(lights[i].type == 1)
        {
            lightDir = normalize(-lights[i].direction);
        }
        else
        {
            lightDir = normalize(lights[i].position - fragPos);
            float distance = length(lights[i].position - fragPos);
            attenuation = 1.0 / (lights[i].constant + lights[i].linear * distance + lights[i].quadratic * distance * distance);
        }

        if(lights[i].type == 3)
        {
            float theta = dot(lightDir, normalize(-lights[i].direction));
            if(theta < lights[i].penumbraAngle) {
                spotlightEffect = 0.0;
            } else if (theta < lights[i].coneAngle) {
                spotlightEffect = smoothstep(lights[i].penumbraAngle, lights[i].coneAngle, theta);
            }
        }

        float diff = max(dot(norm, lightDir), 0.0);

        vec3 specular = vec3(0.0);
        if(specularOn && diff > 0.0)
        {
            vec3 halfwayDir = normalize(lightDir + viewDir);
            float spec = pow(max(dot(norm, halfwayDir), 0.0), materialShininess);
            specular = materialSpecularStrength * spec * lights[i].intensity * lights[i].color;
        }

        vec3 diffuse = lights[i].intensity * diff * lights[i].color;
        finalColor += (diffuse + specular) * spotlightEffect * attenuation;
    }

    FragColor = vec4(ambient, 1.0) + (fragColor * blendedTexture * vec4(finalColor, 1.0));
}