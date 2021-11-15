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

client.on("message", async message => {
    if(message.channel.id == '909826408627462191'){
        const channel = client.channels.cache.get('909901683826499644');
        channel.send("teste");
    }
})

client.on('ready', () => {
    console.log("Connected")
})