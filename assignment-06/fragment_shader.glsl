#version 330

in vec4 fragColor;
in vec2 fragUV;

out vec4 outColor;

uniform sampler2D tex1;
uniform sampler2D tex2;
uniform float blendFactor;

void main()
{
   vec4 texColor1 = texture(tex1, fragUV);
   vec4 texColor2 = texture(tex2, fragUV);
   vec4 blendedColor = mix(texColor1, texColor2, blendFactor);
   outColor = fragColor * blendedColor;
}