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
require('dotenv').config()
client.login(process.env['BOT_TOKEN'])

client.on('ready', () => {
    console.log("Connected")
})

const exampleEmbed = new MessageEmbed()
	.setColor('#0099ff')
	.setTitle('Some title')
	.setDescription('📌$ETH/USDT (SHORT)\nLeverage: 5-10x\nSTATUS UPDATE\nWith price action still ranging around our entries, we can expect to see volume picking up before our weekly close, leading to a complete fill of our orders and a drop towards our targets if our market projection is correct.\nEnjoy bullets🐋')
	.setImage('https://cdn.discordapp.com/attachments/862118738446778422/909560054074703912/unknown.png')
	.setTimestamp()
	.setFooter('Robozão', 'https://uploads.metropoles.com/wp-content/uploads/2018/08/17184217/watchmen-2.jpg');

client.on("message", async message => {
    if(message.content === "/embedtest"){
        const channel = client.channels.cache.get(message.channel.id);
        channel.send({ embeds: [exampleEmbed] });
    }else if(message.content === "/getid"){
        const channel = client.channels.cache.get(message.channel.id);
        channel.send("Channel id: " + message.channel.id);
    }
})