package net.runelite.client.plugins.ChatLogExtended;

import net.runelite.client.config.Config;
import net.runelite.client.config.ConfigGroup;
import net.runelite.client.config.ConfigItem;

@ConfigGroup("ChatLogExtended")
public interface ChatLogExtendedConfig extends Config {

    @ConfigItem(
            keyName = "public",
            name = "Public Chat",
            description = "Enables logging of the public chat"
    )
    default boolean logPublicChat() {
        return false;
    }

    @ConfigItem(
            keyName = "private",
            name = "Private Chat",
            description = "Enables logging of the private chat"
    )
    default boolean logPrivateChat() {
        return false;
    }

    @ConfigItem(
            keyName = "clan",
            name = "Clan Chat",
            description = "Enables logging of the clan chat"
    )
    default boolean logClanChat() {
        return true;
    }
}
