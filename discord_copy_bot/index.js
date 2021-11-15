const Discord = require('discord.js');
const { MessageEmbed } = require('discord.js');
const client  = new Discord.Client({
    allowedMentions:{
        parse: ['users', 'roles'],
        repliedUser: true,
    },
    intents: [
        "GUILDS",
        "GUILD_MEMBERS",
        "GUILD_MESSAGES",
        "GUILD_PRESENCES",
        "GUILD_MESSAGE_REACTIONS"
    ],
});

function creat_embed(color, title, text, image, footer_name, footer_image){
    return new MessageEmbed()
	.setColor(color)
	.setTitle(title)
	.setDescription(text)
	.setImage(image)
	.setTimestamp()
	.setFooter(footer_name, footer_image);
}

client.on("message", async message => {
    if(message.channel.id == process.env['TEST_INPUT_ID']){
        const channel = client.channels.cache.get(process.env['TEST_OUTPUT_ID']);
        var img_url;
        message.attachments.forEach((e)=>{
            img_url = e.url;
        })
        var embed = creat_embed(
            '#0099ff',
            'Trade call',
            message.content,
            img_url, 
            "Robozão", 
            "https://uploads.metropoles.com/wp-content/uploads/2018/08/17184217/watchmen-2.jpg"
        );
        channel.send({ embeds: [embed] });
    }else if(message.channel.id == process.env['INPUT_ID']){
        const channel = client.channels.cache.get(process.env['OUTPUT_ID']);
        var img_url;
        message.attachments.forEach((e)=>{
            img_url = e.url;
        })
        var embed = creat_embed(
            '#0099ff',
            'Trade call',
            message.content,
            img_url, 
            "Robozão", 
            "https://uploads.metropoles.com/wp-content/uploads/2018/08/17184217/watchmen-2.jpg"
        );
        channel.send({ embeds: [embed] });
    }
})

client.on('ready', () => {
    console.log("Connected")
})

require('dotenv').config()
client.login(process.env['BOT_TOKEN'])